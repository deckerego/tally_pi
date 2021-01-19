obs = obslua
settings_cache = {}
light_mapping = {}
idle_color = tonumber('FF0000FF', 16)
idle_brightness = 5
preview_color = tonumber('FF00FF00', 16)
preview_brightness = 5
preview_items = {}
program_color = tonumber('FFFF0000', 16)
program_brightness = 5
program_items = {}
http_timeout_seconds = 4
eligible_input_ids = { "av_capture_input", "droidcam_obs" }

function contains(list, element)
	for _,item in pairs(list) do
		if item == element then
			return true
		end
	end
	return false
end

function script_description()
	return [[
Remote tally lights for camera input sources.
]]
end

function script_defaults(settings)
	obs.obs_data_set_default_int(settings, "IdleColor", tonumber('ffff0000', 16))
	obs.obs_data_set_default_int(settings, "IdleBrightness", 5)
	obs.obs_data_set_default_int(settings, "PreviewColor", tonumber('ff00ff00', 16))
	obs.obs_data_set_default_int(settings, "PreviewBrightness", 5)
	obs.obs_data_set_default_int(settings, "ProgramColor", tonumber('ff0000ff', 16))
	obs.obs_data_set_default_int(settings, "ProgramBrightness", 5)
end

function script_update(settings)
	idle_color = obs.obs_data_get_int(settings, "IdleColor")
	idle_brightness = obs.obs_data_get_int(settings, "IdleBrightness")
	preview_color = obs.obs_data_get_int(settings, "PreviewColor")
	preview_brightness = obs.obs_data_get_int(settings, "PreviewBrightness")
	program_color = obs.obs_data_get_int(settings, "ProgramColor")
	program_brightness = obs.obs_data_get_int(settings, "ProgramBrightness")

	load_input_settings(settings)

	settings_cache = settings
end

function load_input_settings(settings)
	local sources = obs.obs_enum_sources()
	if sources ~= nil then
		for _, source in ipairs(sources) do
			source_id = obs.obs_source_get_id(source)
			if contains(eligible_input_ids, source_id) then
				local source_name = obs.obs_source_get_name(source)
				obs.script_log(obs.LOG_INFO, "Retrieving source: " .. source_name)
				light_mapping[source_name] = obs.obs_data_get_string(settings, source_name)
			end
		end
	end
	obs.source_list_release(sources)
end

function script_properties()
	local props = obs.obs_properties_create()

	obs.obs_properties_add_color(props, "IdleColor", "Idle Color")
	obs.obs_properties_add_int_slider(props, "IdleBrightness", "Idle Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "PreviewColor", "Queued Color")
	obs.obs_properties_add_int_slider(props, "PreviewBrightness", "Queued Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "ProgramColor", "Live Color")
	obs.obs_properties_add_int_slider(props, "ProgramBrightness", "Live Brightness", 0, 10, 1)

	local sources = obs.obs_enum_sources()
	if sources ~= nil then
		for _, source in ipairs(sources) do
			source_id = obs.obs_source_get_id(source)
			if contains(eligible_input_ids, source_id) then
				local source_name = obs.obs_source_get_name(source)
				obs.script_log(obs.LOG_INFO, "Loading source: " .. source_name)
				obs.obs_properties_add_text(props, source_name, source_name .. " light addr:", obs.OBS_TEXT_DEFAULT)
			end
		end
	end
	obs.source_list_release(sources)

	return props
end

function script_load(settings)
	obs.obs_frontend_add_event_callback(handle_event)
end

function handle_event(event)
	if event == obs.OBS_FRONTEND_EVENT_EXIT then
		handle_exit()
	elseif event == obs.OBS_FRONTEND_FINISHED_LOADING then
		handle_loaded()
	elseif event == obs.OBS_FRONTEND_EVENT_SCENE_CHANGED then
		if next(light_mapping) == nil then load_input_settings(settings_cache) end
		handle_program_change()
	elseif event == obs.OBS_FRONTEND_EVENT_PREVIEW_SCENE_CHANGED then
		handle_preview_change()
	end
end

function call_tally_light(source, color, brightness)
	local addr = light_mapping[source]
	if (addr == nil) or (string.len(addr) <= 0) then
		obs.script_log(obs.LOG_INFO, "No tally light set for: " .. source)
		do return end
	end

	local hexColor = string.format("%x", color)
	local hexBlue = string.sub(hexColor, 3, 4)
	local hexGreen = string.sub(hexColor, 5, 6)
	local hexRed = string.sub(hexColor, 7, 8)
	local pctBright = brightness / 10
	local url = "http://" .. addr .. ":7413/set?color=" .. hexRed .. hexGreen .. hexBlue .. "&brightness=" .. pctBright

	local status = os.execute("curl --connect-timeout 5 --max-time 15 '" .. url .. "'  2>&1 &" )
	if status > 0 then
		obs.script_log(obs.LOG_ERROR, "Error connecting to: " .. url)
	end
end

function get_item_names_by_scene(source)
	local item_names = {}
	local scene = obs.obs_scene_from_source(source)
	local scene_name = obs.obs_source_get_name(source)
	local scene_items = obs.obs_scene_enum_items(scene)

	for _, item in pairs(scene_items) do
		local item_source = obs.obs_sceneitem_get_source(item)
		local item_name = obs.obs_source_get_name(item_source)
		if light_mapping[item_name] ~= nil then
			item_names[item_name] = item_name
		end
	end

	obs.sceneitem_list_release(scene_items)
	return item_names
end

function set_lights_by_items(item_names, color, brightness)
	for _, item_name in pairs(item_names) do
		call_tally_light(item_name, color, brightness)
	end
end

function set_idle_lights()
	for src, addr in pairs(light_mapping) do
		if (program_items[src] == nil) and (preview_items[src] == nil) then
			call_tally_light(src, idle_color, idle_brightness)
		end
	end
end

function handle_preview_change()
	local program_source = obs.obs_frontend_get_current_scene()
	local program_name = obs.obs_source_get_name(program_source)
	obs.obs_source_release(program_source);

	local preview_source = obs.obs_frontend_get_current_preview_scene()
	local preview_name = obs.obs_source_get_name(preview_source)

	preview_items = get_item_names_by_scene(preview_source)
	if program_name ~= preview_name then
		set_lights_by_items(preview_items, preview_color, preview_brightness)
	end

	obs.obs_source_release(preview_source)
	set_idle_lights()
end

function handle_program_change()
	local program_source = obs.obs_frontend_get_current_scene()
	program_items = get_item_names_by_scene(program_source)
	set_lights_by_items(program_items, program_color, program_brightness)
	obs.obs_source_release(program_source)
	set_idle_lights()
end

function handle_loaded()
	load_input_settings(settings_cache)
end

function handle_exit()
	for src, addr in pairs(light_mapping.items) do
		call_tally_light(src, "00000000", 0)
	end
end

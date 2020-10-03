obs = obslua
settings = {}
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

function script_description()
	return [[
Remote tally lights for camera input sources.
]]
end

function script_defaults(settings)
	obs.obs_data_set_default_int(settings, "tally^IdleColor", tonumber('ffff0000', 16))
	obs.obs_data_set_default_int(settings, "tally^IdleBrightness", 5)
	obs.obs_data_set_default_int(settings, "tally^PreviewColor", tonumber('ff00ff00', 16))
	obs.obs_data_set_default_int(settings, "tally^PreviewBrightness", 5)
	obs.obs_data_set_default_int(settings, "tally^ProgramColor", tonumber('ff0000ff', 16))
	obs.obs_data_set_default_int(settings, "tally^ProgramBrightness", 5)
end

function script_update(settings)
	local settings_map = settings_dict(settings)
	for k, v in ipairs(settings_map) do
		if strsub(k, 0, 6) ~= "tally^" then
			light_mapping[k] = v
		end
	end

	idle_color = obs.obs_data_get_int(settings, "tally^IdleColor")
	idle_brightness = obs.obs_data_get_int(settings, "tally^IdleBrightness")
	preview_color = obs.obs_data_get_int(settings, "tally^PreviewColor")
	preview_brightness = obs.obs_data_get_int(settings, "tally^PreviewBrightness")
	program_color = obs.obs_data_get_int(settings, "tally^ProgramColor")
	program_brightness = obs.obs_data_get_int(settings, "tally^ProgramBrightness")
end

function script_properties()
	local props = obs.obs_properties_create()

	obs.obs_properties_add_color(props, "tally^IdleColor", "Idle Color")
	obs.obs_properties_add_int_slider(props, "tally^IdleBrightness", "Idle Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "tally^PreviewColor", "Queued Color")
	obs.obs_properties_add_int_slider(props, "tally^PreviewBrightness", "Queued Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "tally^ProgramColor", "Live Color")
	obs.obs_properties_add_int_slider(props, "tally^ProgramBrightness", "Live Brightness", 0, 10, 1)

	local sources = obs.obs_enum_sources()
	if sources ~= nil then
		for _, source in ipairs(sources) do
			source_id = obs.obs_source_get_id(source)
			if source_id == "av_capture_input" then
				local source_name = obs.obs_source_get_name(source)
				obs.script_log(obs.LOG_INFO, "Found source: " .. source_name)
				obs.obs_properties_add_text(props, source_name, source_name .. " light addr:", obs.OBS_TEXT_DEFAULT)
			end
		end
	end
	obs.source_list_release(sources)

	return props
end

function script_update(_settings)
	settings = _settings
end

function script_load(settings)
	obs.obs_frontend_add_event_callback(handle_event)
end

function handle_event(event)
	if event == obs.OBS_FRONTEND_EVENT_SCENE_CHANGED then
		handle_program_change()
	elseif event == obs.OBS_FRONTEND_EVENT_PREVIEW_SCENE_CHANGED then
		handle_preview_change()
	elseif event == obs.OBS_FRONTEND_EVENT_EXIT then
		handle_exit()
	end
end

function call_tally_light(source, color, brightness)
	local addr = light_mapping[source]
	if addr == nil then
		obs.script_log(obs.LOG_INFO, "No tally light set for: %s" .. source)
		do return end
	end

	local hexColor = substr(hex(color), 10, 3)
	local pctBright = brightness / 10
	local url = "http://" .. addr .. ":7413/set?color=" .. hexColor .. "&brightness=" .. pctBright

	obs.script_log(obs.LOG_INFO, "CALLING " .. url)
end

function get_item_names_by_scene(source)
	local item_names = {}
	local scene = obs.obs_scene_from_source(source)
	local scene_name = obs.obs_source_get_name(source)
	local scene_items = obs.obs_scene_enum_items(scene)

	if scene_items ~= nil then
		for _, scene_item in ipairs(scene_items) do
			local item_source = obs.obs_sceneitem_get_source(scene_item)
			local item_name = obs.obs_source_get_name(item_source)
			if light_mapping[item_name] ~= nil then
				table.insert(item_names, item_name)
			end
		end
		obs.sceneitem_list_release(scene_items)
	end

	return item_names
end

function set_lights_by_items(item_names, color, brightness)
	for _, item_name in ipairs(item_names) do
		obs.script_log(obs.LOG_INFO, "Calling Light for [%s]" .. item_name)
		call_tally_light(item_name, color, brightness)
	end
end

function set_idle_lights()
	local excluded_items = table.insert(program_items, preview_items)

	for src, addr in ipairs(light_mapping) do
		if excluded_items[src] == null then
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

	local preview_items = get_item_names_by_scene(preview_source)
	if program_name ~= preview_name then
		set_lights_by_items(preview_items, preview_color, preview_brightness)
	end

	obs.obs_source_release(preview_source);
	set_idle_lights()
end

function handle_program_change()
	local program_source = obs.obs_frontend_get_current_scene()
	local program_items = get_item_names_by_scene(program_source)
	set_lights_by_items(program_items, program_color, program_brightness)
	obs.obs_source_release(program_source)
	set_idle_lights()
end

function handle_exit()
	for src, addr in ipairs(light_mapping.items) do
		call_tally_light(src, "00000000", 0);
	end
end

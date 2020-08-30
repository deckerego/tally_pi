obs = obslua
settings = {}

function script_description()
	return [[
Fire off tally lights
]]
end

function script_properties()
	local props = obs.obs_properties_create()

	local prop = obs.obs_properties_add_list(props, "source", "Camera", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	local sources = obs.obs_enum_sources()
	if sources ~= nil then
		for _, source in ipairs(sources) do
			source_id = obs.obs_source_get_id(source)
			if source_id == "av_capture_input" then
				local source_name = obs.obs_source_get_name(source)
				obs.script_log(obs.LOG_INFO, "Found source: " .. source_name .. ".")
				obs.obs_property_list_add_string(prop, source_name, source_name)
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
		handle_scene_change()
	end
end

function handle_scene_change()
	local scene = obs.obs_frontend_get_current_scene()
	local scene_name = obs.obs_source_get_name(scene)
	obs.script_log(obs.LOG_INFO, "Activating " .. scene_name .. ".")
	obs.obs_source_release(scene);
end

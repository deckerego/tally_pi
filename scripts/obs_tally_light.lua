obs = obslua
http = require("socket.http")
settings = {}

function script_description()
	return [[
Remote tally lights for camera input sources.
]]
end

function script_properties()
	local props = obs.obs_properties_create()

	obs.obs_properties_add_color(props, "idleColor", "Idle Color")
	obs.obs_properties_add_int_slider(props, "idleBrightness", "Idle Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "previewColor", "Queued Color")
	obs.obs_properties_add_int_slider(props, "previewBrightness", "Queued Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "programColor", "Live Color")
	obs.obs_properties_add_int_slider(props, "programBrightness", "Live Brightness", 0, 10, 1)

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
		handle_scene_change()
	end
end

function handle_scene_change()
	local scene = obs.obs_frontend_get_current_scene()
	local scene_name = obs.obs_source_get_name(scene)
	obs.script_log(obs.LOG_INFO, "Activating " .. scene_name .. ".")
	obs.obs_source_release(scene);

	b, c, h = http.request("http://192.168.129.135:7413/status")
	obs.script_log(obs.LOG_INFO, b)
end

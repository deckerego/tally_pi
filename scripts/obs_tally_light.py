import obspython as obs
import urllib.request
import urllib.error

light_mapping = {}
idleColor = '#FF0000FF'
idleBrightness = 5
previewColor = '#FF00FF00'
previewBrightness = 5
programColor = '#FFFF0000'
programBrightness = 5

def call_tally_light():
	color = previewColor[2:7]
	url = 'http://192.168.129.135:7413/set?color=%s' % (color)

	try:
		with urllib.request.urlopen(url) as response:
			data = response.read()
			text = data.decode('utf-8')
			obs.script_log(obs.LOG_INFO, "Tally light: " + text)

	except urllib.error.URLError as err:
		obs.script_log(obs.LOG_WARNING, "Error connecting to tally light URL '" + url + "': " + err.reason)
		obs.remove_current_callback()


def script_description():
	return "Remote tally lights for camera input sources."

def script_defaults(settings):
	obs.obs_data_set_default_string(settings, "idleColor", "#FF0000FF")
	obs.obs_data_set_default_int(settings, "idleBrightness", 5)
	obs.obs_data_set_default_string(settings, "previewColor", "#FF00FF00")
	obs.obs_data_set_default_int(settings, "previewBrightness", 5)
	obs.obs_data_set_default_string(settings, "programColor", "#FFFF0000")
	obs.obs_data_set_default_int(settings, "programBrightness", 5)

def script_update(settings):
	global light_mapping
	global idleColor
	global idleBrightness
	global previewColor
	global previewBrightness
	global programColor
	global programBrightness

	idleColor = obs.obs_data_get_string(settings, "idleColor")
	idleBrightness = obs.obs_data_get_int(settings, "idleBrightness")
	previewColor = obs.obs_data_get_string(settings, "previewColor")
	previewBrightness = obs.obs_data_get_int(settings, "previewBrightness")
	programColor = obs.obs_data_get_string(settings, "programColor")
	programBrightness = obs.obs_data_get_int(settings, "programBrightness")

	sources = obs.obs_enum_sources()
	if sources is not None:
		for source in sources:
			source_id = obs.obs_source_get_id(source)
			if source_id == 'av_capture_input':
				source_name = obs.obs_source_get_name(source)
				tally_addr = obs.obs_data_get_string(settings, source_name)
				obs.script_log(obs.LOG_INFO, "Setting source: " + source_name + " to " + tally_addr)
				light_mapping[source_name] = tally_addr

	obs.source_list_release(sources)

def script_properties():
	props = obs.obs_properties_create()

	obs.obs_properties_add_color(props, "idleColor", "Idle Color")
	obs.obs_properties_add_int_slider(props, "idleBrightness", "Idle Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "previewColor", "Queued Color")
	obs.obs_properties_add_int_slider(props, "previewBrightness", "Queued Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "programColor", "Live Color")
	obs.obs_properties_add_int_slider(props, "programBrightness", "Live Brightness", 0, 10, 1)

	sources = obs.obs_enum_sources()
	if sources is not None:
		for source in sources:
			source_id = obs.obs_source_get_id(source)
			if source_id == 'av_capture_input':
				source_name = obs.obs_source_get_name(source)
				obs.script_log(obs.LOG_INFO, "Found source: " + source_name)
				obs.obs_properties_add_text(props, source_name, source_name + " light addr:", obs.OBS_TEXT_DEFAULT)

	obs.source_list_release(sources)

	return props

def script_update(settings):
	return

def script_load(settings):
	obs.obs_frontend_add_event_callback(handle_event)

def handle_event(event):
	if event is obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
		handle_scene_change()

def handle_scene_change():
	scene = obs.obs_frontend_get_current_scene()
	scene_name = obs.obs_source_get_name(scene)
	obs.script_log(obs.LOG_INFO, "Activating " + scene_name)
	obs.obs_source_release(scene);
	call_tally_light();

import obspython as obs
import json
import urllib.request
import urllib.error

light_mapping = {}
idle_color = int('FF0000FF', 16)
idle_brightness = 5
preview_color = int('FF00FF00', 16)
preview_brightness = 5
preview_items = []
program_color = int('FFFF0000', 16)
program_brightness = 5
program_items = []

def settings_dict(settings):
	settings_json = obs.obs_data_get_json(settings)
	return json.loads(settings_json)

def script_description():
	return "Remote tally lights for camera input sources."

def script_defaults(settings):
	obs.obs_data_set_default_int(settings, "tally^IdleColor", int('ffff0000', 16))
	obs.obs_data_set_default_int(settings, "tally^IdleBrightness", 5)
	obs.obs_data_set_default_int(settings, "tally^PreviewColor", int('ff00ff00', 16))
	obs.obs_data_set_default_int(settings, "tally^PreviewBrightness", 5)
	obs.obs_data_set_default_int(settings, "tally^ProgramColor", int('ff0000ff', 16))
	obs.obs_data_set_default_int(settings, "tally^ProgramBrightness", 5)

def script_update(settings):
	global light_mapping
	global idle_color
	global idle_brightness
	global preview_color
	global preview_brightness
	global program_color
	global program_brightness

	settings_map = settings_dict(settings)
	for k, v in settings_map.items():
		if k[0:6] != "tally^":
			light_mapping[k] = v

	idle_color = obs.obs_data_get_int(settings, "tally^IdleColor")
	idle_brightness = obs.obs_data_get_int(settings, "tally^IdleBrightness")
	preview_color = obs.obs_data_get_int(settings, "tally^PreviewColor")
	preview_brightness = obs.obs_data_get_int(settings, "tally^PreviewBrightness")
	program_color = obs.obs_data_get_int(settings, "tally^ProgramColor")
	program_brightness = obs.obs_data_get_int(settings, "tally^ProgramBrightness")

def script_properties():
	props = obs.obs_properties_create()

	obs.obs_properties_add_color(props, "tally^IdleColor", "Idle Color")
	obs.obs_properties_add_int_slider(props, "tally^IdleBrightness", "Idle Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "tally^PreviewColor", "Queued Color")
	obs.obs_properties_add_int_slider(props, "tally^PreviewBrightness", "Queued Brightness", 0, 10, 1)
	obs.obs_properties_add_color(props, "tally^ProgramColor", "Live Color")
	obs.obs_properties_add_int_slider(props, "tally^ProgramBrightness", "Live Brightness", 0, 10, 1)

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

def script_load(settings):
	obs.obs_frontend_add_event_callback(handle_event)

def handle_event(event):
	if event is obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
		handle_scene_change()
	elif event is obs.OBS_FRONTEND_EVENT_PREVIEW_SCENE_CHANGED:
		handle_preview_change()
	elif event is obs.OBS_FRONTEND_EVENT_EXIT:
		handle_exit()


def call_tally_light(source, color, brightness):
	addr = light_mapping[source]
	if not addr:
		return

	hexColor = hex(color)[10:3:-1]
	pctBright = brightness / 10
	url = 'http://%s:7413/set?color=%s&brightness=%f' % (addr, hexColor, pctBright)

	try:
		with urllib.request.urlopen(url) as response:
			data = response.read()
			text = data.decode('utf-8')
			obs.script_log(obs.LOG_INFO, 'Set %s tally light: %s' % (source, text))

	except urllib.error.URLError as err:
		obs.script_log(obs.LOG_WARNING, 'Error connecting to tally light URL %s: %s' + (url, err.reason))
		obs.remove_current_callback()

def set_scene_light(source, color, brightness) :
	item_names = []
	scene = obs.obs_scene_from_source(source)
	scene_name = obs.obs_source_get_name(source)
	scene_items = obs.obs_scene_enum_items(scene)
	if scene_items is not None:
		for item in scene_items:
			item_source = obs.obs_sceneitem_get_source(item)
			item_name = obs.obs_source_get_name(item_source)
			if item_name in light_mapping:
				item_names.append(item_name)
				obs.script_log(obs.LOG_INFO, 'Calling Light for [%s]: [%s]' % (scene_name, item_name))
				call_tally_light(item_name, color, brightness);
		obs.sceneitem_list_release(scene_items)

	return item_names

def set_idle_lights():
	excluded_items = program_items + preview_items

	for src, addr in light_mapping.items():
		if src not in excluded_items:
			call_tally_light(src, idle_color, idle_brightness);

def handle_preview_change():
	global preview_items

	preview_source = obs.obs_frontend_get_current_preview_scene()
	preview_items = set_scene_light(preview_source, preview_color, preview_brightness)
	obs.obs_source_release(preview_source);
	set_idle_lights()

def handle_scene_change():
	global program_items

	program_source = obs.obs_frontend_get_current_scene()
	program_items = set_scene_light(program_source, program_color, program_brightness)
	obs.obs_source_release(program_source);
	set_idle_lights()

def handle_exit():
	for src, addr in light_mapping.items():
		call_tally_light(src, "00000000", 0);

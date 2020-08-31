import obspython as obs
import urllib.request
import urllib.error

light_mapping = {}
idleColor = int('FF0000FF', 16)
idleBrightness = 5
previewColor = int('FF00FF00', 16)
previewBrightness = 5
programColor = int('FFFF0000', 16)
programBrightness = 5

def script_description():
	return "Remote tally lights for camera input sources."

def script_defaults(settings):
	obs.obs_data_set_default_int(settings, "idleColor", int('ff0000ff', 16))
	obs.obs_data_set_default_int(settings, "idleBrightness", 5)
	obs.obs_data_set_default_int(settings, "previewColor", int('ff00ff00', 16))
	obs.obs_data_set_default_int(settings, "previewBrightness", 5)
	obs.obs_data_set_default_int(settings, "programColor", int('ffff0000', 16))
	obs.obs_data_set_default_int(settings, "programBrightness", 5)

def script_update(settings):
	global light_mapping
	global idleColor
	global idleBrightness
	global previewColor
	global previewBrightness
	global programColor
	global programBrightness

	idleColor = obs.obs_data_get_int(settings, "idleColor")
	idleBrightness = obs.obs_data_get_int(settings, "idleBrightness")
	previewColor = obs.obs_data_get_int(settings, "previewColor")
	previewBrightness = obs.obs_data_get_int(settings, "previewBrightness")
	programColor = obs.obs_data_get_int(settings, "programColor")
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

def script_load(settings):
	obs.obs_frontend_add_event_callback(handle_event)

def handle_event(event):
	if event is obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
		handle_scene_change()

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
		obs.script_log(obs.LOG_WARNING, "Error connecting to tally light URL '" + url + "': " + err.reason)
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
			item_names.append(item_name)
			obs.script_log(obs.LOG_INFO, 'Calling Light for %s: %s' % (scene_name, item_name))
			call_tally_light(item_name, color, brightness);
		obs.sceneitem_list_release(scene_items)

	return item_names

def handle_scene_change():
	done_items = []

	preview_source = obs.obs_frontend_get_current_preview_scene()
	done_items += set_scene_light(preview_source, previewColor, previewBrightness)
	obs.obs_source_release(preview_source);

	program_source = obs.obs_frontend_get_current_scene()
	done_items += set_scene_light(program_source, programColor, programBrightness)
	obs.obs_source_release(program_source);

	for src, addr in light_mapping.items():
		if src not in done_items:
			call_tally_light(src, idleColor, idleBrightness);

bl_info = {
    "name": "NtfyMe Blender",
    "author": "Nanook",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "An unofficial integration of ntfy into Blender",
    "category": "Render",
}

import bpy
import requests
from bpy.app.handlers import persistent
from bpy.props import StringProperty

class NftyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    webhook_url: StringProperty(
        name="Webhook url",
        description="Enter the url of your server",
        default="",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "webhook_url")

class NftyNotificationPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = ""
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.scene, "my_setting", text="Enable Ntfy")

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.prop(context.preferences.addons[__name__].preferences, "webhook_url")

@persistent
def sendNtfy(scene):
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[__name__].preferences
    webhook_url = addon_prefs.webhook_url
    
    if scene.my_setting:
        requests.post(webhook_url,
        data="Your render has finished!",
        headers={
        "Title": "Blender",
        "Priority": "default",
        "Tags": "computer,heavy_check_mark"
    })

def register():
    bpy.utils.register_class(NftyAddonPreferences)
    bpy.utils.register_class(NftyNotificationPanel)
    bpy.app.handlers.render_complete.append(sendNtfy)
    
    bpy.types.Scene.my_setting = bpy.props.BoolProperty(name="Enable Ntfy", default=False)

def unregister():
    bpy.utils.unregister_class(NftyAddonPreferences)
    bpy.utils.unregister_class(NftyNotificationPanel)
    bpy.app.handlers.render_complete.remove(sendNtfy)
    
    del bpy.types.Scene.my_setting

if __name__ == "__main__":
    register()

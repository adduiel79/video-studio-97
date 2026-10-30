import os, threading, json, time, requests
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from plyer import filechooser
API_URL="http://192.168.1.10:8000"  # Set your server LAN/HTTPS address.
# The 97 preset labels are loaded from the backend at startup.
KV="""
<Root>:
    orientation:'vertical'
    padding:'14dp'
    spacing:'9dp'
    canvas.before:
        Color:
            rgba:(.025,.045,.07,1)
        Rectangle:
            pos:self.pos
            size:self.size
    Label:
        text:'VIDEO STUDIO 97'
        color:(.2,.85,.73,1)
        bold:True
        size_hint_y:None
        height:'42dp'
    Label:
        text:root.status
        color:(.8,.88,.95,1)
        size_hint_y:None
        height:'55dp'
    Button:
        text:'Choose video'
        size_hint_y:None
        height:'46dp'
        on_release:root.choose()
    Spinner:
        id:preset
        text:'Loading 97 presets…'
        values:[]
        size_hint_y:None
        height:'50dp'
    Button:
        text:'Process selected preset'
        size_hint_y:None
        height:'50dp'
        on_release:root.process()
    Button:
        text:'Download edited MP4'
        size_hint_y:None
        height:'46dp'
        on_release:root.download()
"""
class Root(BoxLayout):
    status=StringProperty("Connecting to Python processing server…")
    path=None; job_id=None; preset_rows=[]
    def __init__(self,**kw):
        super().__init__(**kw)
        threading.Thread(target=self.load_presets,daemon=True).start()
    def load_presets(self):
        try:
            rows=requests.get(API_URL+"/api/presets",timeout=20).json()
            self.preset_rows=rows
            names=[p["name"] for p in rows]
            self.ids.preset.values=names
            self.ids.preset.text=names[0] if names else "No presets"
            self.status=f"{len(rows)} recipes ready. Choose a video."
        except Exception as e:self.status="Server connection failed: "+str(e)
    def choose(self):filechooser.open_file(on_selection=self.selected)
    def selected(self,sel):
        if sel:self.path=sel[0];self.status="Selected: "+os.path.basename(self.path)
    def process(self):
        if not self.path:self.status="Choose a video first.";return
        name=self.ids.preset.text
        p=next((x for x in self.preset_rows if x["name"]==name),None)
        if not p:self.status="Select a valid preset.";return
        self.status="Uploading and processing…"
        threading.Thread(target=self._process,args=(p,),daemon=True).start()
    def _process(self,p):
        try:
            with open(self.path,"rb") as f:
                r=requests.post(API_URL+"/api/process",files={"video":(os.path.basename(self.path),f)},data={"preset_id":p["id"],"options":json.dumps({})},timeout=180)
            r.raise_for_status();self.job_id=r.json()["job_id"]
            while True:
                j=requests.get(API_URL+"/api/jobs/"+self.job_id,timeout=30).json()
                self.status=f"{p['name']}: {j['status']} {j['progress']}%"
                if j["status"]=="done":self.status="Export complete. Tap Download.";break
                if j["status"]=="error":self.status="Error: "+j.get("error","unknown");break
                time.sleep(2)
        except Exception as e:self.status="Error: "+str(e)
    def download(self):
        if not self.job_id:self.status="No export ready.";return
        try:
            r=requests.get(API_URL+"/api/download/"+self.job_id,timeout=180);r.raise_for_status()
            dest=os.path.join(App.get_running_app().user_data_dir,"edited-video.mp4")
            open(dest,"wb").write(r.content);self.status="Saved to app storage: "+dest
        except Exception as e:self.status="Download failed: "+str(e)
class VideoStudioApp(App):
    def build(self):Builder.load_string(KV);return Root()
if __name__=="__main__":VideoStudioApp().run()

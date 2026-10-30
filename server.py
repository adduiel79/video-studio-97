import json, shutil, subprocess, threading, time, uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

BASE=Path(__file__).parent
DATA=BASE/"data"; INBOX=DATA/"uploads"; OUTBOX=DATA/"exports"
for p in (INBOX,OUTBOX): p.mkdir(parents=True,exist_ok=True)
PRESETS=json.loads(r'[{"id": "p01", "name": "Natural Balance", "category": "Color & Light", "brightness": 0, "contrast": 1.04, "saturation": 1.02}, {"id": "p02", "name": "Bright Daylight", "category": "Color & Light", "brightness": 0.1, "contrast": 1.08, "saturation": 1.08}, {"id": "p03", "name": "Soft Light", "category": "Color & Light", "brightness": 0.06, "contrast": 0.92, "saturation": 0.92}, {"id": "p04", "name": "Warm Glow", "category": "Color & Light", "brightness": 0.04, "contrast": 1.06, "saturation": 1.12}, {"id": "p05", "name": "Cool Clarity", "category": "Color & Light", "brightness": -0.01, "contrast": 1.12, "saturation": 0.92}, {"id": "p06", "name": "Golden Hour", "category": "Color & Light", "brightness": 0.08, "contrast": 1.08, "saturation": 1.18}, {"id": "p07", "name": "Deep Contrast", "category": "Color & Light", "brightness": -0.02, "contrast": 1.28, "saturation": 1.08}, {"id": "p08", "name": "Matte Fade", "category": "Color & Light", "brightness": 0.04, "contrast": 0.88, "saturation": 0.82}, {"id": "p09", "name": "Vivid Pop", "category": "Color & Light", "brightness": 0.02, "contrast": 1.14, "saturation": 1.35}, {"id": "p10", "name": "Pastel Soft", "category": "Color & Light", "brightness": 0.08, "contrast": 0.9, "saturation": 0.78}, {"id": "p11", "name": "Low Light Lift", "category": "Color & Light", "brightness": 0.14, "contrast": 1.12, "saturation": 1.08}, {"id": "p12", "name": "Shadow Detail", "category": "Color & Light", "brightness": 0.09, "contrast": 1.18, "saturation": 0.96}, {"id": "p13", "name": "Clean Whites", "category": "Color & Light", "brightness": 0.03, "contrast": 1.12, "saturation": 0.88}, {"id": "p14", "name": "Rich Color", "category": "Color & Light", "brightness": 0.0, "contrast": 1.1, "saturation": 1.28}, {"id": "p15", "name": "Muted Tones", "category": "Color & Light", "brightness": 0.0, "contrast": 0.96, "saturation": 0.72}, {"id": "p16", "name": "High Key", "category": "Color & Light", "brightness": 0.16, "contrast": 0.92, "saturation": 0.82}, {"id": "p17", "name": "Low Key", "category": "Color & Light", "brightness": -0.1, "contrast": 1.22, "saturation": 0.9}, {"id": "p18", "name": "Cinematic Teal", "category": "Cinematic Looks", "brightness": 0.0, "contrast": 1.16, "saturation": 1.08}, {"id": "p19", "name": "Orange & Teal", "category": "Cinematic Looks", "brightness": 0.02, "contrast": 1.18, "saturation": 1.2}, {"id": "p20", "name": "Blockbuster", "category": "Cinematic Looks", "brightness": 0.0, "contrast": 1.24, "saturation": 1.18}, {"id": "p21", "name": "Moody Drama", "category": "Cinematic Looks", "brightness": -0.08, "contrast": 1.3, "saturation": 0.86}, {"id": "p22", "name": "Blue Steel", "category": "Cinematic Looks", "brightness": -0.03, "contrast": 1.22, "saturation": 0.88}, {"id": "p23", "name": "Warm Film", "category": "Cinematic Looks", "brightness": 0.04, "contrast": 1.1, "saturation": 0.94}, {"id": "p24", "name": "Epic Contrast", "category": "Cinematic Looks", "brightness": -0.04, "contrast": 1.35, "saturation": 1.12}, {"id": "p25", "name": "Soft Cinema", "category": "Cinematic Looks", "brightness": 0.02, "contrast": 0.94, "saturation": 0.88}, {"id": "p26", "name": "Night Scene", "category": "Cinematic Looks", "brightness": -0.12, "contrast": 1.24, "saturation": 0.92}, {"id": "p27", "name": "Desert Cinema", "category": "Cinematic Looks", "brightness": 0.06, "contrast": 1.12, "saturation": 1.08}, {"id": "p28", "name": "Forest Cinema", "category": "Cinematic Looks", "brightness": 0.0, "contrast": 1.12, "saturation": 1.12}, {"id": "p29", "name": "Romantic Film", "category": "Cinematic Looks", "brightness": 0.06, "contrast": 0.96, "saturation": 0.9}, {"id": "p30", "name": "Thriller", "category": "Cinematic Looks", "brightness": -0.1, "contrast": 1.32, "saturation": 0.82}, {"id": "p31", "name": "Documentary", "category": "Cinematic Looks", "brightness": 0.02, "contrast": 1.08, "saturation": 0.94}, {"id": "p32", "name": "Modern Film", "category": "Cinematic Looks", "brightness": 0.0, "contrast": 1.12, "saturation": 1.04}, {"id": "p33", "name": "Silver Screen", "category": "Cinematic Looks", "brightness": -0.02, "contrast": 1.18, "saturation": 0.0}, {"id": "p34", "name": "Vintage Warm", "category": "Vintage & Mono", "brightness": 0.04, "contrast": 0.92, "saturation": 0.78}, {"id": "p35", "name": "Retro 70s", "category": "Vintage & Mono", "brightness": 0.05, "contrast": 0.9, "saturation": 0.82}, {"id": "p36", "name": "Retro 80s", "category": "Vintage & Mono", "brightness": 0.02, "contrast": 1.14, "saturation": 1.2}, {"id": "p37", "name": "Faded Film", "category": "Vintage & Mono", "brightness": 0.08, "contrast": 0.84, "saturation": 0.7}, {"id": "p38", "name": "Sepia Mood", "category": "Vintage & Mono", "brightness": 0.03, "contrast": 0.94, "saturation": 0.48}, {"id": "p39", "name": "Classic B&W", "category": "Vintage & Mono", "brightness": 0.0, "contrast": 1.18, "saturation": 0.0}, {"id": "p40", "name": "High Contrast Mono", "category": "Vintage & Mono", "brightness": 0.0, "contrast": 1.48, "saturation": 0.0}, {"id": "p41", "name": "Soft Mono", "category": "Vintage & Mono", "brightness": 0.04, "contrast": 0.9, "saturation": 0.0}, {"id": "p42", "name": "Noir", "category": "Vintage & Mono", "brightness": -0.1, "contrast": 1.42, "saturation": 0.0}, {"id": "p43", "name": "Old Cinema", "category": "Vintage & Mono", "brightness": 0.02, "contrast": 1.02, "saturation": 0.62}, {"id": "p44", "name": "Instant Photo", "category": "Vintage & Mono", "brightness": 0.06, "contrast": 0.92, "saturation": 0.76}, {"id": "p45", "name": "Dusty Rose", "category": "Vintage & Mono", "brightness": 0.04, "contrast": 0.94, "saturation": 0.82}, {"id": "p46", "name": "Analog Warmth", "category": "Vintage & Mono", "brightness": 0.03, "contrast": 1.02, "saturation": 0.9}, {"id": "p47", "name": "Cold Vintage", "category": "Vintage & Mono", "brightness": -0.02, "contrast": 1.04, "saturation": 0.72}, {"id": "p48", "name": "Classic Newsreel", "category": "Vintage & Mono", "brightness": 0.0, "contrast": 1.22, "saturation": 0.0}, {"id": "p49", "name": "Amber Memory", "category": "Vintage & Mono", "brightness": 0.06, "contrast": 1.0, "saturation": 0.88}, {"id": "p50", "name": "YouTube Punch", "category": "Social & Creator", "brightness": 0.03, "contrast": 1.16, "saturation": 1.24}, {"id": "p51", "name": "Shorts Bright", "category": "Social & Creator", "brightness": 0.08, "contrast": 1.1, "saturation": 1.18}, {"id": "p52", "name": "Reels Pop", "category": "Social & Creator", "brightness": 0.04, "contrast": 1.14, "saturation": 1.3}, {"id": "p53", "name": "TikTok Neon", "category": "Social & Creator", "brightness": 0.02, "contrast": 1.18, "saturation": 1.34}, {"id": "p54", "name": "Travel Color", "category": "Social & Creator", "brightness": 0.05, "contrast": 1.1, "saturation": 1.22}, {"id": "p55", "name": "Food Fresh", "category": "Social & Creator", "brightness": 0.08, "contrast": 1.06, "saturation": 1.3}, {"id": "p56", "name": "Beauty Soft", "category": "Social & Creator", "brightness": 0.1, "contrast": 0.92, "saturation": 0.94}, {"id": "p57", "name": "Product Clean", "category": "Social & Creator", "brightness": 0.04, "contrast": 1.18, "saturation": 0.96}, {"id": "p58", "name": "Gaming Punch", "category": "Social & Creator", "brightness": 0.0, "contrast": 1.28, "saturation": 1.28}, {"id": "p59", "name": "Podcast Warm", "category": "Social & Creator", "brightness": 0.04, "contrast": 1.04, "saturation": 0.94}, {"id": "p60", "name": "Vlog Natural", "category": "Social & Creator", "brightness": 0.03, "contrast": 1.06, "saturation": 1.06}, {"id": "p61", "name": "Wedding Glow", "category": "Social & Creator", "brightness": 0.08, "contrast": 0.96, "saturation": 0.98}, {"id": "p62", "name": "Sports Energy", "category": "Social & Creator", "brightness": 0.0, "contrast": 1.22, "saturation": 1.32}, {"id": "p63", "name": "Street Style", "category": "Social & Creator", "brightness": 0.0, "contrast": 1.26, "saturation": 1.12}, {"id": "p64", "name": "Nature Boost", "category": "Social & Creator", "brightness": 0.04, "contrast": 1.1, "saturation": 1.28}, {"id": "p65", "name": "Portrait Soft", "category": "Social & Creator", "brightness": 0.06, "contrast": 0.94, "saturation": 0.92}, {"id": "p66", "name": "Event Lights", "category": "Social & Creator", "brightness": 0.02, "contrast": 1.18, "saturation": 1.14}, {"id": "p67", "name": "Flip Horizontal", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "mirror": "horizontal"}, {"id": "p68", "name": "Flip Vertical", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "mirror": "vertical"}, {"id": "p69", "name": "Rotate 90 CW", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "rotate": 90}, {"id": "p70", "name": "Rotate 180", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "rotate": 180}, {"id": "p71", "name": "Rotate 90 CCW", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "rotate": 270}, {"id": "p72", "name": "Mirror & Brighten", "category": "Transform & Motion", "brightness": 0.06, "contrast": 1.08, "saturation": 1.05, "mirror": "horizontal"}, {"id": "p73", "name": "Soft Sharpen", "category": "Transform & Motion", "brightness": 0, "contrast": 1.04, "saturation": 1.04, "sharpen": 1}, {"id": "p74", "name": "Detail Sharpen", "category": "Transform & Motion", "brightness": 0, "contrast": 1.12, "saturation": 1.08, "sharpen": 2}, {"id": "p75", "name": "Gentle Blur", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "blur": 1}, {"id": "p76", "name": "Portrait 9:16", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "width": 1080, "height": 1920}, {"id": "p77", "name": "Square 1:1", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "width": 1080, "height": 1080}, {"id": "p78", "name": "Landscape 16:9", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "width": 1920, "height": 1080}, {"id": "p79", "name": "720p Export", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "width": 1280, "height": 720}, {"id": "p80", "name": "1080p Export", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "width": 1920, "height": 1080}, {"id": "p81", "name": "1440p Export", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "width": 2560, "height": 1440}, {"id": "p82", "name": "4K Export", "category": "Transform & Motion", "brightness": 0, "contrast": 1, "saturation": 1, "width": 3840, "height": 2160}, {"id": "p83", "name": "Soft Vignette", "category": "Transform & Motion", "brightness": 0, "contrast": 1.04, "saturation": 0.96, "vignette": 1}, {"id": "p84", "name": "Strong Vignette", "category": "Transform & Motion", "brightness": 0, "contrast": 1.12, "saturation": 0.94, "vignette": 2}, {"id": "p85", "name": "Dreamy Glow", "category": "Creative Effects", "brightness": 0.08, "contrast": 0.92, "saturation": 0.9, "blur": 1}, {"id": "p86", "name": "Bright Pop", "category": "Creative Effects", "brightness": 0.12, "contrast": 1.16, "saturation": 1.2}, {"id": "p87", "name": "Aqua Tone", "category": "Creative Effects", "brightness": 0.02, "contrast": 1.08, "saturation": 1.12}, {"id": "p88", "name": "Magenta Mood", "category": "Creative Effects", "brightness": 0.0, "contrast": 1.12, "saturation": 1.12}, {"id": "p89", "name": "Sunset Fade", "category": "Creative Effects", "brightness": 0.06, "contrast": 0.96, "saturation": 1.06}, {"id": "p90", "name": "Icy Blue", "category": "Creative Effects", "brightness": -0.02, "contrast": 1.12, "saturation": 0.88}, {"id": "p91", "name": "Lush Green", "category": "Creative Effects", "brightness": 0.04, "contrast": 1.08, "saturation": 1.2}, {"id": "p92", "name": "Skin Tone Soft", "category": "Creative Effects", "brightness": 0.05, "contrast": 0.94, "saturation": 0.92}, {"id": "p93", "name": "Crisp Detail", "category": "Creative Effects", "brightness": 0.0, "contrast": 1.2, "saturation": 1.08}, {"id": "p94", "name": "Film Grain Style", "category": "Creative Effects", "brightness": 0.0, "contrast": 1.04, "saturation": 0.92, "grain": 12}, {"id": "p95", "name": "Bright Minimal", "category": "Creative Effects", "brightness": 0.12, "contrast": 0.94, "saturation": 0.88}, {"id": "p96", "name": "Dark Atmosphere", "category": "Creative Effects", "brightness": -0.12, "contrast": 1.2, "saturation": 0.86}, {"id": "p97", "name": "Balanced HDR Look", "category": "Creative Effects", "brightness": 0.03, "contrast": 1.24, "saturation": 1.1}]')
PRESET_MAP={p["id"]:p for p in PRESETS}
app=FastAPI(title="Video Studio 97")
app.mount("/static",StaticFiles(directory=BASE/"web"),name="static")
JOBS={}; LOCK=threading.Lock()

def worker(jid,src,o):
    with LOCK: JOBS[jid].update(status="processing",progress=5)
    out=OUTBOX/f"{jid}.mp4"
    cmd=["ffmpeg","-y","-i",str(src)]
    start=max(0,float(o.get("start",0) or 0)); end=o.get("end")
    if end not in (None,""):
        end=float(end)
        if end<=start:
            with LOCK: JOBS[jid].update(status="error",error="End time must be greater than start time.")
            return
        cmd += ["-ss",str(start),"-t",str(end-start)]
    elif start: cmd += ["-ss",str(start)]
    vf=[]; rot=int(o.get("rotate",0) or 0)
    if rot==90: vf.append("transpose=1")
    elif rot==180: vf += ["hflip","vflip"]
    elif rot==270: vf.append("transpose=2")
    if o.get("mirror")=="horizontal": vf.append("hflip")
    elif o.get("mirror")=="vertical": vf.append("vflip")
    w=int(o.get("width",0) or 0); h=int(o.get("height",0) or 0)
    if w>0 and h>0:
        w=min(w,3840); h=min(h,2160)
        vf.append(f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2")
    b=max(-.5,min(.5,float(o.get("brightness",0) or 0)))
    c=max(.5,min(2,float(o.get("contrast",1) or 1)))
    s=max(0,min(2,float(o.get("saturation",1) or 1)))
    if b or c!=1 or s!=1: vf.append(f"eq=brightness={b}:contrast={c}:saturation={s}")
    if o.get("sharpen"): vf.append(f"unsharp=5:5:{min(2,float(o['sharpen']))}:5:5:0")
    if o.get("blur"): vf.append("boxblur=1:1")
    if o.get("vignette"): vf.append("vignette=PI/5")
    if o.get("grain"): vf.append(f"noise=alls={int(o['grain'])}:allf=t")
    if vf: cmd += ["-vf",",".join(vf)]
    if o.get("mute"): cmd += ["-an"]
    cmd += ["-c:v","libx264","-preset","medium","-crf","22"]
    if not o.get("mute"): cmd += ["-c:a","aac","-b:a","160k"]
    cmd += ["-movflags","+faststart",str(out)]
    with LOCK: JOBS[jid]["progress"]=12
    try:
        p=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
        while p.poll() is None:
            time.sleep(1)
            with LOCK: JOBS[jid]["progress"]=min(94,JOBS[jid]["progress"]+1)
        err=p.stderr.read() if p.stderr else ""
        if p.returncode: raise RuntimeError(err[-1800:] or "FFmpeg failed")
        with LOCK: JOBS[jid].update(status="done",progress=100,output=str(out))
    except Exception as e:
        with LOCK: JOBS[jid].update(status="error",error=str(e)[-1800:])

@app.get("/",response_class=HTMLResponse)
def home(): return (BASE/"web"/"index.html").read_text(encoding="utf-8")
@app.get("/api/health")
def health(): return {"ok":True,"ffmpeg":shutil.which("ffmpeg") is not None}
@app.get("/api/presets")
def presets(): return PRESETS
@app.post("/api/process")
async def process(video:UploadFile=File(...),options:str=Form("{}"),preset_id:str=Form("")):
    if not shutil.which("ffmpeg"): raise HTTPException(500,"FFmpeg is not installed.")
    ext=Path(video.filename or "video.mp4").suffix.lower()
    if ext not in {".mp4",".mov",".mkv",".webm",".avi",".m4v"}: raise HTTPException(400,"Unsupported video format.")
    try: o=json.loads(options)
    except Exception: raise HTTPException(400,"Invalid options JSON.")
    # A preset is a real FFmpeg recipe. Explicit manual values override it only when supplied.
    if preset_id:
        p=PRESET_MAP.get(preset_id)
        if not p: raise HTTPException(400,"Unknown preset.")
        o={**{k:v for k,v in p.items() if k not in ("id","name","category")},**o}
    jid=uuid.uuid4().hex[:12]; src=INBOX/f"{jid}{ext}"
    with src.open("wb") as f:
        while chunk:=await video.read(1024*1024): f.write(chunk)
    with LOCK: JOBS[jid]={"status":"queued","progress":0,"filename":video.filename}
    threading.Thread(target=worker,args=(jid,src,o),daemon=True).start()
    return {"job_id":jid}
@app.get("/api/jobs/{jid}")
def status(jid):
    with LOCK: j=JOBS.get(jid)
    if not j: raise HTTPException(404,"Job not found")
    return {k:v for k,v in j.items() if k!="output"}
@app.get("/api/download/{jid}")
def download(jid):
    with LOCK: j=JOBS.get(jid)
    if not j or j.get("status")!="done": raise HTTPException(404,"Export not ready")
    p=Path(j["output"])
    if not p.exists(): raise HTTPException(404,"Export missing")
    return FileResponse(p,media_type="video/mp4",filename=f"edited-{jid}.mp4")

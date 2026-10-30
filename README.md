# Video Studio 97 — Python Web + Android source

This package provides a dark dashboard inspired by the supplied reference video, with exactly 97 selectable standard editing recipes. Each preset maps to actual FFmpeg filter/transform settings (color grade, rotate/flip, resize, sharpen, blur, vignette, grain, etc.).

No copyright-detection evasion, Content ID bypass, watermark removal, or concealment of copied material is included.

## Web setup
1. Install Python 3.10+ and FFmpeg (ffmpeg must be on PATH).
2. `pip install -r requirements.txt`
3. `uvicorn server:app --host 0.0.0.0 --port 8000`
4. Open `http://127.0.0.1:8000`

## Android APK build
The Android client is in `android/`. Change `API_URL` in `android/main.py` to the address of the computer/server running the API. The Android phone must be able to reach it.

Buildozer requires Linux, Java, Android SDK/NDK and internet access for first-time setup:
```
cd android
pip install buildozer
buildozer android debug
```
The APK is generated in `android/bin/` after a successful build. This execution environment does not have Buildozer or Android SDK/NDK installed, so an APK binary cannot honestly be supplied from here; the complete Android source and build config are included.

For public deployment, add login/authentication, HTTPS, file-size limits, rate limits, persistent job storage, and a cleanup policy. Current jobs are in memory and uploads are local.


## Build APK using only an Android phone
See `ANDROID_FROM_PHONE_BN.md`. A GitHub Actions workflow is included at `.github/workflows/build-apk.yml`; upload the extracted project files to a GitHub repository, then run the workflow and download its APK artifact.

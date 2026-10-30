# শুধু Android ফোন দিয়ে APK বানানোর নিয়ম

এই প্রজেক্টে GitHub Actions workflow যোগ করা আছে। APK আপনার ফোনে নয়, GitHub-এর Ubuntu cloud runner-এ তৈরি হবে; ফোন দিয়ে শুধু আপলোড ও ডাউনলোড করবেন।

## ধাপ
1. ফোনের Chrome-এ https://github.com খুলে একটি account তৈরি/Sign in করুন।
2. `New repository` চাপুন, নাম দিন `video-studio-97`, চাইলে Public রাখুন, তারপর Create repository।
3. রিপোজিটরির `Add file` → `Upload files` দিয়ে ZIP-এর ভেতরের সব ফাইল ও `.github` ফোল্ডারসহ আপলোড করুন। ZIP ফাইলটিকে সরাসরি আপলোড করবেন না—আগে Extract করে ভেতরের ফাইলগুলো আপলোড করুন। লুকানো `.github` ফোল্ডারটি বাদ দেবেন না।
4. `Commit changes` চাপুন।
5. রিপোজিটরির `Actions` ট্যাব খুলুন। `Build Video Studio 97 APK` workflow বেছে `Run workflow` → সবুজ `Run workflow` চাপুন।
6. বিল্ড চলার সময় কয়েক মিনিট থেকে অনেক বেশি সময় লাগতে পারে; প্রথমবার Android SDK/NDK ডাউনলোড হয়। সবুজ টিক এলে workflow run খুলুন।
7. নিচের `Artifacts` অংশে `video-studio-97-apk` চাপলে APK ZIP ডাউনলোড হবে। সেটি Extract করে `.apk` ফাইলটি খুলে Install দিন। Android-এ প্রয়োজন হলে “Install unknown apps” অনুমতি দিন।

## জরুরি কথা
- প্রথমবার বিল্ড ব্যর্থ হলে `Actions`-এর লাল run খুলে শেষের error log দেখুন; Buildozer dependency বা Android recipe-র কারণে retry/সমন্বয় লাগতে পারে।
- GitHub-এর private repository এবং Actions ব্যবহারে account plan অনুযায়ী usage limit থাকতে পারে।
- এই APK হলো Android Kivy client। ভিডিও প্রসেসিংয়ের জন্য `server.py` চালানো API server-এ ফোন থেকে সংযোগ লাগবে। `android/main.py`-এর `API_URL`-এ আপনার API server-এর HTTPS address বসাতে হবে; শুধু APK ইনস্টল করলেই সব ৯৭টি preset অফলাইনে চলবে না।
- অপরিচিত কারও APK install করবেন না; নিজের GitHub Actions build থেকেই APK নিন।

# Waifuku

## Author
hilmo

## Description
pecinta waifu ternyata seorang info stealer? hahh 🥶🥶
bongkar semua kedoknya dia

format flag: FindITCTF\<flag\>

## TLDR
1. cek website, nemu obfuscated js
2. deobfuscate js
3. ketemu bot tele di jsnya
4. dump semua message dari bot tele + channel id yang ada
5. download waifu.exe
6. cek pake wireshark, nemu url skemer.find-it.id
7. dynamic analysis waifu.exe pakai frida
8. dapet ps1 script
9. dari info" diatas + chat tele yang bilang suruh cek port di nama channel discord ctf findit (channelnya hidden, harus pakai discord plugin. dapet 4000)
10. intercept traffic dari waifu.exe ke skemer.find-it.id:4000
11. dapet flag
12. decrypt flag dari ps1 sebelumnya
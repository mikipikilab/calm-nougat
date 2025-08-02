nsoa mjs naprqavio  prvo ov @echo off
echo === Inicijalizacija Git repozitorijuma ===
git init

echo === Dodavanje svih fajlova ===
git add .

echo === Kreiranje commit-a ===
git commit -m "Prvi upload Flask projekta"

echo === Postavljanje grane main ===
git branch -M main

echo === Dodavanje GitHub repozitorijuma (ako ne postoji) ===
git remote | find "origin"
if %errorlevel% neq 0 (
    git remote add origin https://github.com/mikipikilab/calm-nougat.git
)

echo === Slanje na GitHub ===
git push -u origin main

pause

@echo off
echo === Dodavanje svih izmena ===
git add .

echo === Kreiranje commit-a ===
set /p msg="Unesi opis izmjena: "
git commit -m "%msg%"

echo === Slanje na GitHub ===
git push

echo === Zavr�eno! Render ce automatski napraviti novi deploy. ===
pause

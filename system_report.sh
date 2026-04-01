#!/bin/bash
DATE=$(date)
echo "=== 시스템 리포트 ===" >> ~/git-practice/report.txt
echo "날짜: $DATE" >> ~/git-practice/report.txt
echo "사용자: Junyong" >> ~/git-practice/report.txt
echo "디스크: $(df -h / | tail -1)" >> ~/git-practice/report.txt
echo "메모리: $(free -h | grep Mem)" >> ~/git-practice/report.txt
echo "-------------------" >> ~/git-practice/report.txt
git add .
git commit -m "auto report"
git push origin main

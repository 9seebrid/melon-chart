# -*- coding: utf-8 -*-
"""
멜론 차트 PyQt 프로그램 - 포트폴리오용 CSV 저장 버전

정리 포인트
1. DB 기능 제거
2. 멜론 차트 조회 + 화면 표시 + CSV 저장에 집중
3. 역할별 함수 분리
4. 예외 처리/메시지 정리
5. 포트폴리오에서 설명하기 좋은 구조로 단순화

전제
- 기존 UI 파일(music_UI.py)의 위젯 이름을 그대로 사용
  * btn_del      : 상태 변경 버튼(이제 CSV 저장 버튼으로 사용)
  * btn_insert   : 데이터 삽입 버튼(이제 선택 항목 저장 or 전체 저장 버튼으로 변경 가능)
  * btn_listUp   : 리스트 불러오기 버튼
  * db_list      : 왼쪽 리스트 영역
  * melon_list   : 오른쪽 리스트 영역

권장 UI 문구 변경
- "현재 리스트" -> "저장된 CSV 미리보기"
- "멜론 리스트" -> "멜론 차트"
- "상태 변경" -> "CSV 저장"
- "데이터 삽입" -> "선택 곡 저장" 또는 "전체 저장"
- "리스트 불러오기" -> "차트 불러오기"
"""

# ==============================
# 표준 라이브러리
# ==============================
import os
import sys
import csv
from datetime import datetime

# ==============================
# 서드파티 라이브러리
# ==============================
import requests
from bs4 import BeautifulSoup
import PyQt5

# Qt plugin path 설정
plugin_path = os.path.join(os.path.dirname(PyQt5.__file__), "Qt5", "plugins", "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog

# ==============================
# 프로젝트 내부 파일
# ==============================
import music_UI


class MainDialog(QDialog, music_UI.Ui_dialog):
    """멜론 차트를 조회하고 CSV로 저장하는 메인 다이얼로그"""

    def __init__(self):
        super().__init__(None)
        self.setupUi(self)

        # 현재 조회된 차트 데이터를 메모리에 보관
        self.chart_data = []
        self.last_saved_file = ""

        # 버튼 연결
        self.btn_listUp.clicked.connect(self.load_chart)        # 차트 조회
        self.btn_insert.clicked.connect(self.save_chart_csv)    # CSV 저장
        self.btn_del.clicked.connect(self.preview_saved_csv)    # CSV 불러오기

        # 시작 안내 문구
        self.initialize_view()

    def initialize_view(self):
        """프로그램 시작 시 화면 초기화"""
        self.db_list.clear()
        self.melon_list.clear()

        self.db_list.append("저장된 CSV를 불러오면 이 영역에 미리보기가 표시됩니다.")
        self.melon_list.append("[안내] '리스트 불러오기' 버튼을 눌러 멜론 차트를 조회하세요.")

    # =========================================================
    # UI 이벤트 함수
    # =========================================================
    def load_chart(self):
        """멜론 차트를 조회해서 화면에 출력"""
        self.db_list.clear()
        self.melon_list.clear()

        try:
            self.chart_data = self.fetch_melon_chart(limit=100)

            if not self.chart_data:
                self.show_error("멜론 차트 데이터를 가져오지 못했습니다.")
                return

            for item in self.chart_data:
                line = f"{item['rank']}위 | {item['title']} | {item['artist']}"
                self.melon_list.append(line)

            self.db_list.append(f"차트 {len(self.chart_data)}건을 조회했습니다.")
            self.db_list.append("CSV 저장 버튼을 눌러 파일로 저장할 수 있습니다.")

            self.show_ok("멜론 차트 조회 완료")

        except Exception as e:
            self.show_error(f"멜론 차트 조회 실패\n{e}")

    def save_chart_csv(self):
        """현재 조회된 차트 데이터를 CSV 파일로 저장"""
        if not self.chart_data:
            self.show_error("저장할 데이터가 없습니다. 먼저 차트를 불러오세요.")
            return

        confirm = QMessageBox.question(
            self,
            "확인",
            "현재 멜론 차트를 CSV 파일로 저장하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.No:
            return

        default_name = f"melon_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "CSV 저장",
            default_name,
            "CSV Files (*.csv)",
        )

        if not file_path:
            return

        try:
            self.write_csv(file_path, self.chart_data)
            self.last_saved_file = file_path

            self.db_list.clear()
            self.db_list.append("CSV 저장 완료")
            self.db_list.append(file_path)
            self.db_list.append("")
            self.db_list.append("상위 10건 미리보기")

            for item in self.chart_data[:10]:
                preview_line = f"{item['rank']}위 | {item['title']} | {item['artist']}"
                self.db_list.append(preview_line)

            self.show_ok(f"CSV 저장 완료\n{file_path}")

        except Exception as e:
            self.show_error(f"CSV 저장 실패\n{e}")

    def preview_saved_csv(self):
        """저장된 CSV 파일을 다시 열어서 왼쪽 영역에 미리보기"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "CSV 파일 선택",
            "",
            "CSV Files (*.csv)",
        )

        if not file_path:
            return

        try:
            self.db_list.clear()
            rows = self.read_csv(file_path)

            if not rows:
                self.db_list.append("CSV 파일이 비어 있습니다.")
                return

            self.db_list.append(f"파일명: {file_path}")
            self.db_list.append(f"총 {len(rows)}건")
            self.db_list.append("")

            for row in rows[:20]:
                line = f"{row['rank']}위 | {row['title']} | {row['artist']}"
                self.db_list.append(line)

            self.show_ok("CSV 미리보기 완료")

        except Exception as e:
            self.show_error(f"CSV 파일 불러오기 실패\n{e}")

    # =========================================================
    # 핵심 기능 함수
    # =========================================================
    def fetch_melon_chart(self, limit=100):
        """멜론 차트 페이지에서 곡 정보를 수집"""
        url = "https://www.melon.com/chart/index.htm"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        titles = soup.find_all("div", {"class": "ellipsis rank01"})
        artists = soup.find_all("div", {"class": "ellipsis rank02"})
        album_images = soup.find_all("a", {"class": "image_typeAll"})

        title_list = []
        artist_list = []
        image_list = []

        for title_tag in titles:
            a_tag = title_tag.find("a")
            title_list.append(a_tag.text.strip() if a_tag else "제목 없음")

        for artist_tag in artists:
            span_tag = artist_tag.find("span", {"class": "checkEllipsis"})
            artist_list.append(span_tag.text.strip() if span_tag else "가수 정보 없음")

        for image_tag in album_images:
            img_tag = image_tag.find("img")
            image_url = ""
            if img_tag:
                image_url = img_tag.get("src", "").strip()
            image_list.append(image_url)

        max_count = min(limit, len(title_list), len(artist_list), len(image_list))
        chart_data = []

        for i in range(max_count):
            chart_data.append(
                {
                    "rank": i + 1,
                    "title": title_list[i],
                    "artist": artist_list[i],
                    "album_image": image_list[i],
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        return chart_data

    def write_csv(self, file_path, data):
        """차트 데이터를 CSV 파일로 저장"""
        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["rank", "title", "artist", "album_image", "collected_at"],
            )
            writer.writeheader()
            writer.writerows(data)

    def read_csv(self, file_path):
        """CSV 파일을 읽어서 리스트로 반환"""
        with open(file_path, mode="r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            return list(reader)

    # =========================================================
    # 공통 메시지 함수
    # =========================================================
    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("오류")
        msg.setText("작업 실패")
        msg.setInformativeText(message)
        msg.exec_()

    def show_ok(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("알림")
        msg.setText("작업 완료")
        msg.setInformativeText(message)
        msg.exec_()


# =============================================================
# 프로그램 실행
# =============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = MainDialog()
    main_dialog.show()
    app.exec_()

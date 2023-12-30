import tkinter as tk
from PIL import ImageGrab
import webbrowser
import os

class ScrapCollectionApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # 처음에 윈도우를 숨김
        self.root.title("Scrap Collection App")
        self.root.attributes('-alpha', 0.2)  # 전체 윈도우의 투명도 설정

        # 위젯창 생성
        self.widget_window = tk.Toplevel(root)
        self.widget_window.geometry("200x100+1720+780")  # 오른쪽 하단에서 20픽셀씩 떨어진 위치
        self.widget_window.attributes('-topmost', True)  # 항상 다른 창 위에 나타나도록 함
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # 투명 이미지를 배경으로 사용하는 캔버스 생성
        self.transparent_canvas = tk.Canvas(self.root, width=screen_width-200, height=screen_height, bg="SystemTransparent")
        print("transparent")
        #마우스 이벤트 바인딩
        self.transparent_canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.transparent_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.transparent_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # 변수 초기화
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.canvas_visible = False
        self.image_index = 0  # 이미지 저장 횟수
        # Scrap 버튼과 Collection 버튼 추가
        self.scrap_button = tk.Button(self.widget_window, text="Scrap", command=self.toggle_canvas)
        self.scrap_button.pack()

        self.collection_button = tk.Button(self.widget_window, text="Collection", command=self.open_webpage)
        self.collection_button.pack()

                # 이미지 저장 경로 설정
        self.image_folder = "/Users/yunrry/Desktop/MyShowroom/assets"
        # showroom.html 파일 경로 설정
        self.showroom_path = "/Users/yunrry/Desktop/MyShowroom/myshowroom.html"

        # 기존 showroom.html 파일 읽어오기
        with open(self.showroom_path, 'r', encoding='utf-8') as f:
            self.showroom_content = f.read()


    def toggle_canvas(self):
  
        if self.canvas_visible:  # 캔버스가 보이는 상태인지 확인
       
            self.transparent_canvas.pack_forget()  # 캔버스를 숨김
        else:
            self.root.deiconify()
            self.transparent_canvas.pack()  # 캔버스를 다시 보이게 함
            print("pack")

        # self.canvas_visible = not self.canvas_visible  # 상태를 토글

        



    def on_mouse_press(self, event):
        # 마우스 누른 위치 저장
        self.start_x = self.transparent_canvas.canvasx(event.x)
        self.start_y = self.transparent_canvas.canvasy(event.y)

        # 이전에 그려진 사각형 삭제
        if self.rect_id:
            self.transparent_canvas.delete(self.rect_id)

    def on_mouse_drag(self, event):
        # 마우스를 떼어진 위치까지의 사각형 영역 그리기
        cur_x = self.transparent_canvas.canvasx(event.x)
        cur_y = self.transparent_canvas.canvasy(event.y) - 20

        if self.rect_id:
            self.transparent_canvas.delete(self.rect_id)

        # 이전 좌표와 현재 좌표 중 더 작은 값을 사용하여 캡처 영역 설정
        x = min(self.start_x, cur_x)
        y = min(self.start_y, cur_y)
        width = abs(self.start_x - cur_x)
        height = abs(self.start_y - cur_y)

        # 사각형 그리기
        self.rect_id = self.transparent_canvas.create_rectangle(int(x), int(y), round(x + width), round(y + height), outline="red")

    def save_image(self, screenshot):
        self.image_index += 1
        image_filename = f"captured_{self.image_index}.png"
        image_path = os.path.join(self.image_folder, image_filename)
        screenshot.save(image_path)
        print("Image saved successfully!")

        # 새로운 이미지 태그 생성
        new_image_tag = f'<img src="assets/{image_filename}" alt="Captured Image" width="200">'
        # showroom.html에 새로운 이미지 태그 추가
        self.showroom_content += new_image_tag

        # showroom.html 파일 업데이트
        with open(self.showroom_path, 'w', encoding='utf-8') as f:
            f.write(self.showroom_content)

    def on_mouse_release(self, event):
        # 사용자가 영역을 선택한 경우에만 capture 수행
        if self.rect_id:
            self.transparent_canvas.delete(self.rect_id)

        cur_x = self.transparent_canvas.canvasx(event.x)
        cur_y = self.transparent_canvas.canvasy(event.y)

        if self.start_x is not None and self.start_y is not None:
            x = min(self.start_x, cur_x)
            y = min(self.start_y, cur_y) + 30
            width = abs(self.start_x - cur_x)
            height = abs(self.start_y - cur_y)

            # 영역의 넓이가 0인 경우 예외처리
            if width == 0 or height == 0:
                print("영역의 넓이가 0입니다. 캡처되지 않았습니다.")
            else:
                # 윈도우 캡처
                screenshot = ImageGrab.grab(bbox=(round(x + 10), round(y + 25), int(x + width), int(y + height)))
                print(screenshot)
                # 이미지 저장
                print("Saving image to:", self.image_folder)
                try:
                    self.save_image(screenshot)
                    # print("Image saved successfully!")
                    # 캔버스를 숨기기
                    self.root.withdraw() #윈도우를 숨김
                    self.transparent_canvas.pack_forget()
                except Exception as e:
                    print("Error saving image:", e)


                # Scrap 버튼 다시 활성화
                self.scrap_button.config(state=tk.NORMAL)

        # 그려진 사각형 삭제
        self.transparent_canvas.delete(self.rect_id)

    def open_webpage(self):
        # 웹페이지 실행 및 이미지 로드
        web_page = "file://" + os.path.abspath("/Users/yunrry/Desktop/MyShowroom/myshowroom.html")
        webbrowser.open(web_page)

if __name__ == "__main__":
    # assets 폴더 생성
    os.makedirs("assets", exist_ok=True)

    # Tkinter 애플리케이션 실행
    root = tk.Tk()
    app = ScrapCollectionApp(root)
    root.mainloop()

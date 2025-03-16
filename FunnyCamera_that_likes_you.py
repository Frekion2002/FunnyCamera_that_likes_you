import cv2 as cv
import time

# VideoCapture 객체 생성 (기본 카메라: 인자 0)
camera = cv.VideoCapture(0)

# VideoWriter 설정
fourcc = cv.VideoWriter_fourcc(*'XVID')
frame_width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = camera.get(cv.CAP_PROP_FPS)
Funny_Camera = cv.VideoWriter('FunnyCamera.avi', fourcc, fps, (frame_width, frame_height))

# 모드 설정: Preview 모드는 False, Record 모드는 True
record_mode = False
cnt = 0 # 꺼지지 않는 카메라 설정
display_message = False # 메세지 표시 여부
message_end_time = 0 # 메세지 종료 시간 저장장
infrared_mode = False # 적외선선 처리

while True:
    vaild, frame = camera.read()  # 카메라에서 프레임 읽기
    if not vaild:
        break

    frame_real_save = frame.copy()

    if infrared_mode:
        frame = cv.applyColorMap(cv.cvtColor(frame, cv.COLOR_BGR2GRAY), cv.COLORMAP_JET)
        frame_real_save = cv.applyColorMap(cv.cvtColor(frame_real_save, cv.COLOR_BGR2GRAY), cv.COLORMAP_JET)

    # Record 모드인 경우 화면에 표시 (빨간색 원)
    if record_mode:
        cv.circle(frame, (20, 20), 10, (0, 0, 255), -1)
        Funny_Camera.write(frame_real_save)  # 동영상 파일로 저장

    if display_message:
        current_time = time.time()
        if cnt == 1:
            cv.putText(frame, "Are you really...going to turn me off?", (80, 280), cv.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 2)
        elif cnt == 2:
            cv.putText(frame, "Are you seriously...going to leave me?", (80, 280), cv.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 2)
        
        # 메세지 표시 시간 초과 시 제거거
        if current_time > message_end_time:
            display_message = False

    if cnt == 3:
        cv.putText(frame, "Fine! I'll disappear! Live well and take care~!", (80, 280), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 2)
        cv.imshow('FunnyCamera', frame)
        cv.waitKey(2000) # 2초동안 기다림
        break

    # 화면에 프레임 표시
    cv.imshow('FunnyCamera', frame)

    # 키 입력 처리
    key = cv.waitKey(1)
    if key == 27:  # ESC 키
        cnt += 1
        if cnt == 1 or cnt == 2:
            display_message = True
            message_end_time = time.time() + 2
    elif key == ord(' '):  # Space 키
        if record_mode:
            record_mode = False
        else:
            record_mode = True  # 모드 전환
    elif key == ord('\t'):
        if infrared_mode:
            infrared_mode = False
        else:
            infrared_mode = True  # 모드 전환

# 자원 해제
camera.release()
Funny_Camera.release()
cv.destroyAllWindows()
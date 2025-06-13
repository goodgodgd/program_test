import os
import shutil

def rename_files(src_path, dst_path):
    """
    src_path의 파일들을 규칙에 따라 새로운 이름으로 dst_path에 복사합니다.

    - 파일 이름 규칙: 'midterm' 문자열로 시작하는 부분부터 끝까지 사용
    - 예: '김경원_1788_2432274_midterm_KKW22.py' -> 'midterm_KKW22.py'

    :param src_path: 원본 파일들이 있는 디렉터리 경로
    :param dst_path: 파일을 복사할 대상 디렉터리 경로
    """
    # 1. 복사할 대상 디렉터리가 없으면 생성합니다.
    os.makedirs(dst_path, exist_ok=True)

    # 2. 기준이 될 키워드를 정의합니다.
    keyword = "midterm"

    # 3. 소스 디렉터리의 모든 파일 목록을 가져옵니다.
    try:
        file_list = os.listdir(src_path)
    except FileNotFoundError:
        print(f"오류: 소스 경로 '{src_path}'를 찾을 수 없습니다.")
        return

    # 4. 각 파일을 순회하며 작업합니다.
    for filename in file_list:
        # 5. 파일 이름 안에 키워드가 있는지 확인하고 시작 위치를 찾습니다.
        start_index = filename.find(keyword)

        # 키워드가 파일 이름에 포함되어 있다면
        if start_index != -1:
            # 6. 'midterm'부터 끝까지 잘라 새 파일 이름을 만듭니다.
            new_filename = filename[start_index:]

            # 7. 원본과 대상 파일의 전체 경로를 생성합니다.
            full_src_path = os.path.join(src_path, filename)
            full_dst_path = os.path.join(dst_path, new_filename)

            # 8. 파일을 복사합니다.
            print(f"'{filename}' -> '{new_filename}' 복사 완료")
            shutil.copy2(full_src_path, full_dst_path)

    print(f"\n총 {len(file_list)}개 파일 처리가 완료되었습니다.")


if __name__ == "__main__":
    rename_files("F:/work/program_test/submitted_src", "F:/work/program_test/submitted")
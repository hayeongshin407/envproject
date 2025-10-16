import streamlit as st
import time

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="생태 탐험가 여권", page_icon="🗺️")

# --- 미션에 사용할 데이터 (선생님 버전 유지) ---
ZONES = ['열대', '사막', '지중해', '온대', '극지']
MISSIONS_DATA = {
    '열대': {
        'icon': '🌴',
        'description': """
        ### 🌴 열대 기후란?
        일 년 내내 평균 기온이 18℃ 이상으로 높고, 비가 많이 내리는 기후입니다. 
        
        ### 대표 동식물은?
        - **동물:** 아마존의 포식자 **피라냐**, 살아있는 화석 **나일악어** 등을 볼 수 있어요.
        - **식물:** 고무나무, 카카오나무 등 키가 큰 나무들이 많아 마치 정글 같아요.
        """,
        'quiz_question': '열대 기후에 대한 설명으로 틀린 것은 무엇일까요?',
        'quiz_options': ['일 년 내내 날씨가 덥다.', '피라냐, 나일악어 같은 동물이 산다.', '춥고 건조해서 눈이 많이 내린다.'],
        'quiz_answer': '춥고 건조해서 눈이 많이 내린다.',
        'mission_image': 'images/tropical_mission.jpg',
        'mission_target': '피라냐'
    },
    '사막': {
        'icon': '🌵',
        'description': """
        ### 🌵 사막 기후란?
        비가 거의 오지 않아 매우 건조하고, 낮과 밤의 온도 차이가 매우 큰 기후입니다.
        
        ### 대표 동식물은?
        - **동물:** 큰 귀로 열을 식히는 **사막여우**, 등에 혹은 지방을 저장하는 **낙타**가 살아요.
        - **식물:** 몸에 물을 저장하기 위해 잎이 가시로 변한 **선인장**이 대표적이에요.
        """,
        'quiz_question': '사막 기후의 특징으로 틀린 것은?',
        'quiz_options': ['비가 거의 오지 않는다', '선인장이 산다', '일 년 내내 비가 많이 온다'],
        'quiz_answer': '일 년 내내 비가 많이 온다',
        'mission_image': 'images/desert_mission.jpg',
        'mission_target': '아가베'
    },
    '지중해': {
        'icon': '🌿',
        'description': """
        ### 🌿 지중해 기후란?
        여름은 덥고 건조하지만, 겨울은 따뜻하고 비가 자주 내리는 기후입니다. 
        
        ### 대표 동식물은?
        - **동물:** 도마뱀과 같은 파충류를 볼 수 있어요.
        - **식물:** **올리브나무**, **포도나무**, 향기로운 허브 식물들이 잘 자라요.
        """,
        'quiz_question': '지중해 기후에서 잘 자라는 식물이 아닌 것은?',
        'quiz_options': ['올리브나무', '포도나무', '야자수'],
        'quiz_answer': '야자수',
        'mission_image': 'images/mediterranean_mission.jpg',
        'mission_target': '올리브나무'
    },
    '온대': {
        'icon': '🍂',
        'description': """
        ### 🍂 온대 기후란?
        우리나라처럼 봄, 여름, 가을, 겨울의 사계절 변화가 뚜렷하게 나타나는 기후입니다.
        
        ### 대표 동식물은?
        - **동물:** **다람쥐**, 너구리 등 우리에게 친숙한 동물들이 살아요.
        - **식물:** 가을에 예쁘게 물드는 **단풍나무**, 늘 푸른 **소나무** 등을 볼 수 있어요.
        """,
        'quiz_question': '온대 기후의 가장 큰 특징은 무엇일까요?',
        'quiz_options': ['사계절이 뚜렷하다', '항상 덥다', '얼음으로 덮여 있다'],
        'quiz_answer': '사계절이 뚜렷하다',
        'mission_image': 'images/dolhareubang.jpg',
        'mission_target': '돌하르방'
    },
    '극지': {
        'icon': '❄️',
        'description': """
        ### ❄️ 극지 기후란?
        일 년 내내 기온이 매우 낮아 춥고, 땅이 두꺼운 얼음과 눈으로 덮여있는 기후입니다. 
        
        ### 대표 동식물은?
        - **동물:** **턱끈펭귄**, **북극곰**, 물범 등이 추위에 적응하며 살아가요.
        - **식물:** 이끼 종류와 같은 몇몇 식물만 자랄 수 있어요.
        """,
        'quiz_question': '극지방에 사는 동물이 아닌 것은?',
        'quiz_options': ['펭귄', '북극곰', '코알라'],
        'quiz_answer': '코알라',
        'mission_image': 'images/polar_mission.jpg',
        'mission_target': '반달가슴곰'
    }
}

# --- 앱 상태 초기화 함수 ---
def initialize_state():
    st.session_state.page = 'home'
    st.session_state.stamps = {zone: False for zone in ZONES + ['히든']}
    st.session_state.quiz_passed = {zone: False for zone in ZONES}
    for zone in ZONES:
        st.session_state[f'mission_{zone}_step'] = 1

if 'page' not in st.session_state:
    initialize_state()

# --- 페이지를 구성하는 공통 함수들 ---
def show_info_page(zone_name):
    data = MISSIONS_DATA[zone_name]
    st.title(f"{data['icon']} {zone_name}기후 알아보기") 
    st.markdown(data['description'])
    if st.button("내용을 다 읽었어요! 퀴즈 풀기", key=f"info_btn_{zone_name}"):
        st.session_state.page = f'quiz_{zone_name}'
        st.rerun()

def show_quiz_page(zone_name):
    data = MISSIONS_DATA[zone_name]
    st.title(f"✍️ {zone_name}관 퀴즈")
    st.subheader(data['quiz_question'])
    
    user_answer = st.radio("정답을 골라주세요.", data['quiz_options'], key=f"quiz_{zone_name}")
    
    if st.button("정답 제출", key=f"quiz_btn_{zone_name}"):
        if user_answer == data['quiz_answer']:
            st.session_state.quiz_passed[zone_name] = True
            st.success("정답입니다! 이제 사진 미션을 수행할 수 있어요.")
            time.sleep(2)
            st.session_state.page = f'mission_{zone_name}'
            st.rerun()
        else:
            st.error("아쉬워요, 내용을 다시 한번 확인해볼까요?")
            if st.button("설명 다시 보기", key=f"reread_btn_{zone_name}"):
                st.session_state.page = f'info_{zone_name}'
                st.rerun()

def mission_page_default(zone_name, target_name, image_path):
    mission_step_key = f'mission_{zone_name}_step'
    st.title(f"📸 {zone_name}관 사진 미션")
    st.info("아래 사진 속 동/식물을 찾아주세요!") 
    st.image(image_path)
    if st.session_state.get(mission_step_key, 1) == 1:
        st.subheader("1. 먼저 인증샷을 찍어주세요!")
        picture = st.camera_input("카메라를 눌러 사진 찍기", key=f"camera_{zone_name}")
        if picture:
            st.session_state[mission_step_key] = 2
            st.rerun()
    elif st.session_state.get(mission_step_key) == 2:
        st.success("사진이 잘 찍혔어요!")
        st.subheader("2. 이제 이름을 아래에 적어주세요.")
        user_answer = st.text_input(f"찾은 동/식물의 이름은 무엇인가요?", key=f"text_{zone_name}")
        if st.button("최종 제출하기", type="primary", key=f"submit_{zone_name}"):
            if user_answer.strip() == target_name:
                st.session_state.stamps[zone_name] = True
                st.success(f"정답입니다! {zone_name}관 도장을 획득했습니다.")
                st.balloons()
                time.sleep(2)
                st.session_state.page = 'home'
                st.rerun()
            else:
                st.error("이름이 틀렸어요. 이름표를 다시 확인해볼까요?")

def show_passport():
    st.title("나의 생태 탐험가 여권")
    st.subheader("내가 모은 기후 도장")
    st.markdown("---")
    cols = st.columns(len(ZONES) + 1)
    for i, zone in enumerate(ZONES + ['히든']):
        with cols[i % len(cols)]:
            st.write(f"**{zone}**")
            if st.session_state.stamps.get(zone, False):
                st.success("✔️ 획득")
            else:
                st.write("미획득")

with st.sidebar:
    st.header("메뉴")
    if st.button("메인 화면"):
        st.session_state.page = 'home'
        st.rerun()
    if st.button("내 여권 보기"):
        st.session_state.page = 'passport'
        st.rerun()
    st.markdown("---")
    # '탐험 초기화' 버튼 로직 수정
    if st.button("탐험 초기화"):
        initialize_state()
        st.rerun()

# --- 페이지 라우팅 (보여줄 화면 결정) ---
current_page = st.session_state.page

if current_page == 'home':
    st.title("🗺️ 생태 탐험가 여권")
    st.header("5대 기후관을 탐험하고 모든 도장을 모아보세요!")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3, col1, col2] 
    for i, zone in enumerate(ZONES):
        with columns[i]:
            if st.button(f"{MISSIONS_DATA[zone]['icon']} {zone}관 입장", disabled=st.session_state.stamps.get(zone, False), key=f"btn_{zone}"):
                st.session_state.page = f'info_{zone}'
                st.rerun()
            if st.session_state.stamps.get(zone, False):
                st.success(f"✔️ {zone}관 완료!")
    
    all_regular_missions_done = all(st.session_state.stamps.get(zone, False) for zone in ZONES)
    
    if all_regular_missions_done and not st.session_state.stamps.get('히든', False):
        st.markdown("---")
        st.warning("✨ 모든 도장을 모았군요! 히든 미션이 나타났습니다! ✨")
        if st.button("⭐ 히든 미션 도전하기"):
            st.session_state.page = 'mission_hidden'
            st.rerun()

elif current_page == 'passport':
    show_passport()

# ############ 이 부분이 수정되었습니다! (페이지 이동 로직 순서 변경) ############
# 구체적인 페이지(온대, 히든, 최종)를 먼저 확인합니다.
elif current_page == 'mission_온대':
    if st.session_state.quiz_passed.get('온대', False):
        st.title("🍂 온대관 사진 미션")
        st.info("아래 사진 속 '돌하르방'을 찾아서 똑같이 사진을 찍어주세요!")
        st.image(MISSIONS_DATA['온대']['mission_image'])
        picture = st.camera_input("카메라를 눌러 인증샷 찍기")
        if picture:
            st.success("사진이 찍혔습니다! 아래 사진을 선생님께 보여주세요.")
            st.image(picture)
            if st.button("선생님께 확인받았어요!", type="primary"):
                st.session_state.stamps['온대'] = True
                st.success("미션 성공! 온대관 도장을 획득했습니다.")
                st.balloons()
                time.sleep(2)
                st.session_state.page = 'home'
                st.rerun()
    else:
        st.warning("퀴즈를 먼저 통과해야 미션을 수행할 수 있어요!")
        if st.button("퀴즈 풀러 가기"):
            st.session_state.page = 'quiz_온대'
            st.rerun()

elif current_page == 'mission_hidden':
    st.title("⭐ 히든 미션 ⭐")
    st.info("사진 속 코알라를 찾아 인증샷을 찍어주세요!")
    st.image("images/koala.jpg")
    
    picture = st.camera_input("카메라를 눌러 히든 미션 인증샷 찍기")
    
    if picture:
        st.success("히든 미션 사진 확인! 아래 사진을 선생님께 보여주세요.")
        st.image(picture)

        if st.button("선생님께 최종 확인받았어요!", type="primary"):
            st.session_state.stamps['히든'] = True
            st.success("히든 미션 성공! 당신을 진정한 생태 탐험가로 임명합니다!")
            st.balloons()
            time.sleep(3)
            st.session_state.page = 'final_end'
            st.rerun()

elif current_page == 'final_end':
    st.title("🏆 진정한 생태 탐험가 탄생! 🏆")
    st.header("모든 미션과 히든 미션까지 완벽하게 해결했습니다!")
    st.write("오늘의 즐거운 탐험을 기억하며, 앞으로도 우리 지구를 사랑하는 멋진 사람이 되어주세요!")
    st.balloons()

# 일반적인 페이지(info_, quiz_, mission_)를 나중에 확인합니다.
elif current_page.startswith('info_'):
    zone_name = current_page.split('_')[1]
    show_info_page(zone_name)

elif current_page.startswith('quiz_'):
    zone_name = current_page.split('_')[1]
    show_quiz_page(zone_name)
    
elif current_page.startswith('mission_'):
    zone_name = current_page.split('_')[1]
    if st.session_state.quiz_passed.get(zone_name, False):
        if zone_name in MISSIONS_DATA:
            mission_info = MISSIONS_DATA[zone_name]
            mission_page_default(zone_name=zone_name, 
                                 target_name=mission_info['mission_target'], 
                                 image_path=mission_info['mission_image'])
    else:
        st.warning("퀴즈를 먼저 통과해야 미션을 수행할 수 있어요!")
        if st.button("퀴즈 풀러 가기"):
            st.session_state.page = f'quiz_{zone_name}'
            st.rerun()
# #############################################################
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
st.header('Daegu')
list = ['Spark Land:ferris_wheel:', 'Kim Kwangseok Road🎸', 'E-World:roller_coaster:', '83 Tower:tokyo_tower:', 'Elybaden:swimmer:']
tab1, tab2, tab3, tab4, tab5 = st.tabs(list)

def tabs(tabnum, name, googlelink, intro, image1, image2, data, pos, neg, image3):
    with (tabnum):
        st.subheader(name)
        # st.markdown('**Train: 3hrs 24 min / Bus: 5hrs 2 min** (departure from seoul)')
        col1, col2, col3, col4 = st.columns([1.5,1.3,1,1])
        with col1:
            st.markdown('**How To Get There:**')
        with col2:
            st.page_link(googlelink, label='Google Map', icon='🗺️')
        with col3:
            st.page_link('https://www.letskorail.com/ebizbf/EbizbfForeign_pr16100.do?gubun=1',
                         label='Train', icon='🚃')
        with col4:
            st.page_link('https://www.kobus.co.kr/main.do',
                         label='bus', icon='🚌')

        # st.markdown('**Introduction**')
        with st.container(height=200):
            st.markdown(intro)
        st.divider()

        col1, col2 = st.columns([1,1])

        with col1:
            st.markdown('**Image**')
            st.image(image1,
                     use_column_width=True)

        with col2:
            st.markdown('**You may also like 😃**')
            row1 = st.columns(2)
            row2 = st.columns(2)
            for i, col in enumerate(row1 + row2):
                tile = col.expander(rec_place[i])
                tile.image(rec_place_img[i],
                     caption=rec_caption[i],
                     use_column_width=True)

        st.divider()

        col1, col2 = st.columns([1,1])

        with col1:
            st.markdown('💡**Highlights of the Destination**')
            st.text('(Top Keywords based on Korean blog)')
            st.image(image2,
                     use_column_width=True)
        with col2:
            data1 = pd.read_csv(data)
            data1[['Year', 'Month', 'Day']] = data1['날짜'].str.rstrip('.').str.split('.', expand=True)
            # 전체 데이터에서 모든 월을 추출
            all_months = data1['Month'].unique()

            # 'month' 리스트 생성
            month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                          'October', 'November', 'December']

            # 월 이름 리스트를 전체 월 중 있는 월만 남기도록 필터링
            filtered_month_list = [month_list[int(month) - 1] for month in all_months]
            # popular_month 만들기
            popular_month = pd.DataFrame(data1['Month'].value_counts().sort_index())
            popular_month['month'] = filtered_month_list

            # 후기수 가장 많은 달 1위 뽑기
            mon = popular_month.sort_values(by='count', ascending=False)['month'][0]
            st.markdown(f'**🗓️ Most Visited Month: :red[{mon}]**')

            st.text('(based on Korean reviews)')
            fig = px.pie(popular_month, values='count',
                         names='month', hover_data=['count'],
                         labels={'count': 'Count'},
                         width=400, height=400, hole=0.3)

            fig.update_traces(textinfo='percent+label', textfont_size=14, textposition='inside')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

        st.divider()

        total_count = pos + neg
        st.markdown(f'🔍The reviews from korean visitors are generally like this (**{total_count} reviews**)')
        positive_ratio = (pos / total_count) * 100
        negative_ratio = (neg / total_count) * 100

        positive_icon = '😊'  # 긍정을 나타내는 이모티콘
        negative_icon = '😞'  # 부정을 나타내는 이모티콘

        positive_display = f'{positive_icon} {positive_ratio:.0f}%'
        negative_display = f'{negative_icon} {negative_ratio:.0f}%'

        st.subheader(f'**:green[{positive_display}]** **:red[{negative_display}]**')

        with st.expander('Review text positive/negative word distribution (Bigram NetworkX Graph)'):
            st.image(image3, use_column_width=True)

# 스파크랜드--------------------------------------------------------------------------------------

#관광지명
name = list[0]
#관광지 구글 링크
googlelink = 'https://www.google.com/maps/place/%EC%8A%A4%ED%8C%8C%ED%81%AC%EB%9E%9C%EB%93%9C/data=!3m1!4b1!4m6!3m5!1s0x3565e30a0e206a57:0x91e07d1d64b0ec5!8m2!3d35.8686818!4d128.5987188!16s%2Fg%2F11h71mx2n9?entry=ttu'
#관광지 소개 글
intro = '''Spark Land, nestled in downtown Daegu, is a dynamic fusion of a shopping mall and theme park. It boasts an 
        array of attractions, including a fashion street, a selection of restaurants and cafés, amusement rides, 
        and indoor sports facilities. A standout feature is the ferris wheel, uniquely designed with a reinforced glass 
        floor, offering visitors a remarkable experience. From atop the ferris wheel, panoramic views of Dongseong-ro 
        and the wider Daegu cityscape unfold. As evening sets in, the Sky Lounge and Spark Sky are bathed in night 
        lights, transforming the atmosphere into something even more enchanting.'''
#추천 장소 4곳
rec_place = ['Dongseong-ro Street', 'Crazy Pang Pang', 'Daegu Modernization Street', 'Cheongna Hill']
#추천 장소 이미지 경로 4개
rec_place_img = ['img/dayul/dongseongro.jpg',
                 'img/dayul/crazypang.jpg',
                 'img/dayul/geundahwa.jpg',
                 'img/dayul/cheongra.jpg']
#추천 장소 설명 4개
rec_caption = ["Daegu's largest downtown area and landmark",
               "The only indoor multi-extreme park in South Korea",
               "A street in Daegu where the past, present, and future coexist",
               "Historic missionary site in Daegu, featuring ivy-lined paths, landmarks, and film sets."]
# 관광지 Image
image1 = 'img/dayul/sparkland.png'
#Wordcloud
image2 = 'img/dayul/sparklandwc.png'
#파이차트 경로
data = 'data/daegu/sparkland.csv'
#Positive 개수
pos_cnt = 85
#Negative 개수
neg_cnt = 40
#Bigram NetworkX Graph 이미지 첨부
image3 = 'img/dayul/sparklandgraph.png'

#tabnum만 바꿔주기 (tab1, tab2, tab3, tab4, tab5)
tabs(tab1, name, googlelink, intro, image1, image2, data, pos_cnt, neg_cnt, image3)

# 김광석다시그리기길-----------------------------------------------------------------------------------------------
#관광지명
name = list[1]
#관광지 구글 링크
googlelink = 'https://www.google.com/maps/place/Kim+Gwang-Seok+Street/data=!3m1!4b1!4m6!3m5!1s0x3565e3ca16f6867f:0xf9ee18e975905b1!8m2!3d35.859905!4d128.6065957!16s%2Fg%2F11c5rwxrp5?entry=ttu'
#관광지 소개 글
intro = '''Kim Kwangseok-gil Street is a mural street near Bangcheon Market in the neighborhood where musician Kim 
        Kwang-seok used to live prior to his passing. The 350 meter-long wall has statues and murals depicting his 
        life and music. Every autumn, the area of Bangcheon Market and Dongseongno hosts a “Kim Kwang-seok Singing 
        Contest” in his memory.'''
#추천 장소 4곳
rec_place = ['Apsan Mountain Observatory', 'Suseongmot Lake Resort',
             'Daegu Dalseong Park', 'Apsan Cable Car ']
#추천 장소 이미지 경로 4개
rec_place_img = ['img/dayul/apsanjeonmangdae.jpg',
                 'img/dayul/suseongmot.jpg',
                 'img/dayul/dalsong.jpg',
                 'img/dayul/apsancable2.jpeg']
#추천 장소 설명 4개
rec_caption = ["Sunset Point: Capturing Daegu's landscape in one glance at dusk.",
               "Ideal for family outings and romantic dates with diverse attractions.",
               "A park cherished by the people of Daegu, steeped in history.",
               "A must-visit spot for sightseeing in Daegu, offering a panoramic view of the city center."]
# 관광지 Image
image1 = 'img/dayul/kimgwangseokgil.jpg'
#Wordcloud
image2 = 'img/dayul/kimgwangseokwc.png'
#파이차트 경로
data = 'data/daegu/kimgwangsuk.csv'
#Positive 개수
pos_cnt = 41
#Negative 개수
neg_cnt = 21
#Bigram NetworkX Graph 이미지 첨부
image3 = 'img/dayul/kimgwangseokgraph.png'
#tabnum만 바꿔주기 (tab1, tab2, tab3, tab4, tab5)
tabs(tab2, name, googlelink, intro, image1, image2, data, pos_cnt, neg_cnt, image3)

# 이월드-----------------------------------------------------------------------------------------------
#관광지명
name = list[2]
#관광지 구글 링크
googlelink = 'https://www.google.com/maps/place/E-World/data=!3m1!4b1!4m6!3m5!1s0x3565e480f56ff341:0x3aef1b939bba3f21!8m2!3d35.8533511!4d128.5638836!16s%2Fg%2F1thcq6b2?entry=ttu'
#관광지 소개
intro = '''In October 1987, E-World began construction on a tower and theme park, completed the master plan for the 
        construction in 1993, and opened it in March 1995. It is a European-style city park decorated with waterfalls, 
        fountains, lights, and flowers, with rides, exhibitions, art spaces, and restaurants that all ages can enjoy. 
        There are theme plazas to provide novelty and enjoyment for visitors at E-World. Representative plazas include 
        the entrance plaza near the ticket office, the central plaza located in Fantasy World, Children's Square with 
        a playground for kids, and Youngtown Square for young people.
'''
#추천 장소 4곳
rec_place = ['Geumho River Cherry Blossom Tunnel', 'Arte Suseong Land',
             'Jumunjin Breakwater', 'Jeongdongsimgok Badabuchae Trail']
#추천 장소 이미지 경로 4개
rec_place_img = ['img/dayul/geumhogang.jpg',
                 'img/dayul/아르떼.JPG',
                 'img/dayul/seongdangmok.jpg',
                 'img/dayul/dongchon.jpg']
#추천 장소 설명 4개
rec_caption = ['It is famous for its cherry blossoms.',
               'The first amusement park in Daegu',
               'A resting place for citizens, beautiful in all four seasons',
               'There are various recreational facilities and well-built roads for enjoyable drives.']
# 관광지 Image
image1 = 'img/dayul/eworld.png'
#Wordcloud
image2 = 'img/dayul/daegueworldwc.png'
#파이차트 경로
data = 'data/daegu/daegueworld.csv'
#Positive 개수
pos_cnt = 7
#Negative 개수
neg_cnt = 4
#Bigram NetworkX Graph 이미지 첨부
image3 = 'img/dayul/daegueworldgraph.png'
#tabnum만 바꿔주기 (tab1, tab2, tab3, tab4, tab5)
tabs(tab3, name, googlelink, intro, image1, image2, data, pos_cnt, neg_cnt, image3)

# 83타워 -------------------------------------------------------------------------------

#관광지명
name = list[3]
#관광지 구글 링크
googlelink = 'https://www.google.com/maps/place/Daegu+83+Tower/data=!3m1!4b1!4m6!3m5!1s0x3565e480574187d9:0xf93f6ce0fde7999!8m2!3d35.8533043!4d128.5665671!16s%2Fm%2F0gwzphh?entry=ttu'
#관광지 소개 글
intro = '''83 Tower is a symbol of Daegu and offers an incredible view of the entire city. 
        The tower also has a revolving restaurant and Sky Lounge, offering top cuisine and night views of the city.
'''
#추천 장소 4곳
rec_place = ['Daegu Arboretum', 'Palgongsan Cable Car', 'Hwawon Park', 'Ancient Tombs in Bullo-dong']
#추천 장소 이미지 경로 4개
rec_place_img = ['img/dayul/daegusumok.jpg',
                 'img/dayul/palgonsan.jpg',
                 'img/dayul/hwanwon.jpg',
                 'img/dayul/gobungun.jpg']
#추천 장소 설명 4개
rec_caption = ['A resting space for citizens of Daegu, where various plant species inhabit.',
               'You can enjoy the scenery while also experiencing thrills at the same time.',
               'a vast park beside the Nakdonggang River, is steeped in history',
               'Clusters of tombs from the Three Kingdoms period, ranging from large to small in size.']
# 관광지 Image
image1 = 'img/dayul/83tower.png'
#Wordcloud
image2 = 'img/dayul/83towerwordcloud.png'
#파이차트 경로
data = 'data/daegu/83tower.csv'
#Positive 개수
pos_cnt = 24
#Negative 개수
neg_cnt = 18
#Bigram NetworkX Graph 이미지 첨부
image3 = 'img/dayul/83towergraph.png'
#tabnum만 바꿔주기 (tab1, tab2, tab3, tab4, tab5)
tabs(tab4, name, googlelink, intro, image1, image2, data, pos_cnt, neg_cnt, image3)

# 엘리바덴-------------------------------------------------------------------------------

#관광지명
name = list[4]
#관광지 구글 링크
googlelink = 'https://www.google.com/maps/place/Spa+Elybaden/data=!3m1!4b1!4m6!3m5!1s0x3565fad7eb24d317:0x94e222a24e6aea51!8m2!3d35.8248737!4d128.5257702!16s%2Fg%2F11fy4pym8v?entry=ttu'
#관광지 소개 글
intro = '''A multifaceted resort in the city center, offering unique spas featuring ginseng and red ginseng, a 
        traditional Korean sauna heated with firewood, and an 800-square-meter kids' park, Ellymong, the largest 
        in Daegu, along with Fitniss, a hotspot for modern health management.'''
#추천 장소 4곳
rec_place = ['Daegu Spa Valley', 'Life Spa', 'Nature Park', 'Palgongsan Shimcheon Land']
#추천 장소 이미지 경로 4개정동진해변
rec_place_img = ['img/dayul/spabelly.jpg',
                 'img/dayul/saenhwaloncheon.jpg',
                 'img/dayul/naturepark.jpg',
                 'img/dayul/simcheonland.jpg']
#추천 장소 설명 4개
rec_caption = ['A year-round water park offering various water attractions and hot springs',
               'Urban Health Hot Springs',
               'The botanical garden consists of a glasshouse zoo and a radial outdoor zoo.',
               'The purest natural spring water, untouched by purification processes, the finest natural hot spring.']
# 관광지 Image
image1 = 'img/dayul/elevaden.jpg'
#Wordcloud
image2 = 'img/dayul/elevadaenwc.png'
#파이차트 경로
data = 'data/daegu/elevaden.csv'
#Positive 개수
pos_cnt = 59
#Negative 개수
neg_cnt = 59
#Bigram NetworkX Graph 이미지 첨부
image3 = 'img/dayul/elevadaengraph.png'
#tabnum만 바꿔주기 (tab1, tab2, tab3, tab4, tab5)
tabs(tab5, name, googlelink, intro, image1, image2, data, pos_cnt, neg_cnt, image3)
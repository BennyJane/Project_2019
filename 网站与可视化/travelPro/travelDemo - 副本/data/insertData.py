import pandas as pd


def insertVideo(db, Video):
    videoDf = pd.read_csv('./data/video.csv')
    videoDf = videoDf.drop_duplicates(['id'])
    videoDf = videoDf[videoDf['title'] is not None]
    origin_data = videoDf.to_dict(orient='split')['data']
    all_videos = []
    for eachData in origin_data:
        all_videos.append(
            Video(
                id=eachData[0],
                title=eachData[1],
                img=eachData[2],
                actors=eachData[3],
                director=eachData[4],
                brief=eachData[5],
                goal=eachData[6],
                category=eachData[7],
                isCrawl=eachData[8],
                isIndex=eachData[9]
            )
        )
    db.session.add_all(all_videos)
    db.session.commit()


def insertBelong(db, Belong):
    originDf = pd.read_csv('./data/belongInfo.csv')
    origin_data = originDf.to_dict(orient='split')['data']
    all_videos = []
    for eachData in origin_data:
        all_videos.append(
            Belong(
                id=eachData[0],
                video_belong_id=eachData[1],
                video_id=eachData[2],
            )
        )
    db.session.add_all(all_videos)
    db.session.commit()

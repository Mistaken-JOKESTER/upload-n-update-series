class Configuration:

    tmdb_video_folder_path = "E:\\upwork\\upload_files\\video"
    tmdb_subtitle_folder_path = "E:\\upwork\\upload_files\\subtitle"

    aws_access_key_id='UGX4JHE8NIVFU9P5I8SF'
    aws_secret_access_key='HlyoGzz4ke1R7ZAbdN0kBliOTVwgQgm2ezJWvPR9'

    # subtitle bucket
    sub_region_name='ap-northeast-1'
    sub_endpoint_url='https://s3.ap-northeast-1.wasabisys.com'
    sub_bucket_name = 'swipesub'

    # episode bucket
    ep_region_name='us-central-1'
    ep_endpoint_url='https://s3.us-central-1.wasabisys.com'
    ep_bucket_name = 'seeds'

    light_sail_ip = '172.104.102.39'
    light_sail_user = 'ubuntu'
    ssh_file_path = 'imdb7.plus.pem'

    db = 'imdb7_plus'
    title_collection = "movie_n_series"
    episode_details_collection = 'episode_details'

    log_flag=True
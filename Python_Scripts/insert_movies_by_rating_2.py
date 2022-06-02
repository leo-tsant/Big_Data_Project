from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra import ConsistencyLevel
from cassandra.query import BatchStatement, SimpleStatement, BatchType
from cassandra.policies import RetryPolicy
import pandas as pd

cloud_config = {
    'secure_connect_bundle': '/home/leotsant/Downloads/secure-connect-big-data-project-cluster.zip'
}
auth_provider = PlainTextAuthProvider(
    'MyrrlmamdWZRMrQhSwUIeyNx', 'KzmZYIBZ4p0K_8RYYdldNqlA1rHs-l-LGEcG.lSSSFsqcwbR9siBZmF6jWW5C9s.Bh+zz3ZGjJvYnc,Rt-QiziY+KWul0Yr9u_mNnpUXMoynR+6TWuqvoDhcqER+SMNr')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('big_data')

row = session.execute("select release_version from system.local").one()


# Read Files
rating_data = pd.read_csv(
    "/home/leotsant/Downloads/MovieLens_Dataset/rating.csv")

rating_data['timestamp'] = pd.to_datetime(rating_data['timestamp'])

query = "INSERT INTO movies_by_rating (movie_id, rating, user_id, timestamp) VALUES (?,?,?,?) IF NOT EXISTS"
prepared = session.prepare(query)

j = 0
while j < len(rating_data.movieId):
    session.execute_async(
        prepared, (rating_data.movieId[j], rating_data.rating[j], rating_data.userId[j], rating_data.timestamp[j]))
    j += 1

if row:
    print("Success!")
else:
    print("An error occurred.")

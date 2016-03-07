from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = "224655598-i1Ut3hpHlBrm8GZsF5VtY6DcJ8XShAB5bof7sKvR"
access_token_secret = "2WB1R6FEFyjOXel3cMzbOATUrxMETtUG54P7WbWeAH2k3"
consumer_key = "Zd9Ab5KvjQ8OgOsOIS6sRVP05"
consumer_secret = "Nwi9xwNBg08LlMpaFao6B2Twgg3Ki0oYsI4tKnDqdCcsN5v6f4"

class StdOutListener(StreamListener):
	def on_data(self, data):
		print data
		return True
		
	def on_error(self, status):
		print status
		
if __name__ == '__main__':
	#This handles Twitter authentication and the connection to Twitter Streaming API
	l= StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	
	#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	stream.filter(track=['#TVK', '#The Voice Kids'])
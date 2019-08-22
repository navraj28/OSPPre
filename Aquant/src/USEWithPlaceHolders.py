import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity

#Initialize Tensorflow Graph & Universal Sentence Encoder
def init():
    global g, session, embedded_text, text_input
    # Create graph and finalize (finalizing optional but recommended).
    g = tf.Graph()
    with g.as_default():
        # We will be feeding 1D tensors of text into the graph.
        text_input = tf.compat.v1.placeholder(dtype=tf.string, shape=[None])
        embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-large/3")
        embedded_text = embed(text_input)
        init_op = tf.group([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])
    g.finalize()

    # Create session and initialize.
    session = tf.compat.v1.Session(graph=g)
    session.run(init_op)

#Use Tensorflow Graph & Universal Sentence Encoder
def get_features(texts):
    if type(texts) is str:
        texts = [texts]

    result1 = session.run(embedded_text, feed_dict={text_input: texts})
    result1 = result1.reshape(len(texts) , 512)
    return result1

def cosineSimilarity(v1, v2):
    v1R = v1.reshape(1 , 512)
    v2R = v2.reshape(1 , 512)
    return cosine_similarity(v1R, v2R)
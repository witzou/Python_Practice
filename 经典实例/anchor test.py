import tensorflow as tf

base_anchor_size = 256
anchor_scales = [0.5, 1, 2]
anchor_ratios = [0.5, 1, 2]

base_anchor = tf.constant([0, 0, base_anchor_size, base_anchor_size], tf.float32)  # [x_center, y_center, w, h]

def enum_scales(base_anchor, anchor_scales):

    anchor_scales = base_anchor * tf.constant(anchor_scales, dtype=tf.float32, shape=(len(anchor_scales), 1))

    return anchor_scales


def enum_ratios(anchors, anchor_ratios):
    '''
    ratio = h /w
    :param anchors:
    :param anchor_ratios:
    :return:
    '''
    ws = anchors[:, 2]  # for base anchor: w == h
    hs = anchors[:, 3]
    sqrt_ratios = tf.sqrt(tf.constant(anchor_ratios))

    ws = tf.reshape(ws / sqrt_ratios[:, tf.newaxis], [-1, 1])
    hs = tf.reshape(hs * sqrt_ratios[:, tf.newaxis], [-1, 1])

    return hs, ws

with tf.Session() as sess:
    anchors = enum_scales(base_anchor, anchor_scales)
    ws, hs = enum_ratios(anchors, anchor_ratios)  # per locations ws and hs
    print('clw: anchors = ', sess.run(anchors))
    print('clw: ws = ', sess.run(ws))
    print('clw: hs = ', sess.run(hs))
    print('end!')
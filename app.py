#!/usr/bin/env python3
"""A simple application to demo Thoth's software stack recommendations."""

import sys
import tensorflow as tf
import time


def thoth_hello():
    """Print hello world from within a TensorFlow session."""
    while True:
        hello = tf.constant('Hello Thoth by TensorFlow!')
        sess = tf.Session()
        print(sess.run(hello))
        time.sleep(3)


if __name__ == '__main__':
    sys.exit(thoth_hello())

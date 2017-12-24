import os
import tensorflow as tf

from config import cfg
from model_eval import evaluate 
from capsnet import CapsNet

def main(_):
    dataset = cfg.dataset
    if dataset == 'mnist':
        input_shape = (cfg.batch_size, 28, 28, 1)
    elif dataset == 'affnist':
        input_shape = (cfg.batch_size, 40, 40, 1)
    else:
        raise ValueError("{} is not an available dataset".format(dataset))
    
    tf.logging.info("Initializing CNN for {}...".format(dataset))
    model = CapsNet(input_shape=input_shape, is_training=False)
    tf.logging.info("Finished initialization.")

    if not os.path.exists(cfg.logdir):
        os.mkdir(cfg.logdir)
    logdir = os.path.join(cfg.logdir, model.name)
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logdir = os.path.join(logdir, dataset)
    if not os.path.exists(logdir):
        os.mkdir(logdir)

    sv = tf.train.Supervisor(graph=model.graph, logdir=logdir, save_model_secs=0)

    tf.logging.info("Initialize evaluation...")
    evaluate(model, sv, dataset)
    tf.logging.info("Finished evaluation.")

    
if __name__ == '__main__':
    tf.app.run()
 
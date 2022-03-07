# Copyright (c) 2022 RWTH Aachen - Werkzeugmaschinenlabor (WZL)
# Contact: Simon Cramer, s.cramer@wzl-mq.rwth-aachen.de

from absl import logging,flags,app
import feature_selection_principal_component_analysis as fspca
from s3_smart_open import read_pd_fth, read_pckl, to_pd_fth, to_pckl

flags.DEFINE_string('input_path',None, 'path for input data')
flags.DEFINE_string('output_path',None, 'path for saving selected features')
flags.DEFINE_enum('stage','fit',['fit','transform', 'inverse'],'Wether to fit_transform or only transform a dataframe or inverse scale to recieve original data.')
flags.DEFINE_string('filename_x',None,'Name of feature dataframe to perform pca transformation.')
flags.DEFINE_string('filename_y',None,'Name of target dataframe. It is not required for the pca but it will be copied from the input path to the output path.')
flags.DEFINE_float('total_variance', 1, 'Sum of variances of the individual principal components')
flags.DEFINE_string('pca_object',None,'Filename of the pca object for transfrom and inverse transform')

flags.mark_flag_as_required('input_path')
flags.mark_flag_as_required('output_path')
flags.mark_flag_as_required('filename_x')

FLAGS = flags.FLAGS

def main(argv):
    """Runs a PCA (Principal component analysis)

    Args:
        argv (None): No further arguments should be parsed

    Raises:
        ValueError: If input path is not existent
        ValueError: If output path is not existent
        ValueError: If filename_x is not existent
    """        
    del argv 

    df_x = read_pd_fth(FLAGS.input_path, FLAGS.filename_x)

    if not FLAGS.pca_object:
        pca_object_name = 'pca.pckl'
    else:
        pca_object_name = FLAGS.pca_object

    if FLAGS.stage == 'fit':
        x, pca_obj = fspca.pca(x=df_x, total_variance=FLAGS.total_variance, pca=None)
    else:
        pca_obj = read_pckl(FLAGS.input_path, pca_object_name)

        if FLAGS.stage == "inverse":
            x, pca_obj = fspca.inverse_pca(df_x, pca_obj)
        elif FLAGS.stage == "transform":
            x, pca_obj = fspca.pca(x=df_x, total_variance=None, pca=pca_obj)
    
    if FLAGS.filename_y:
        df_y = read_pd_fth(FLAGS.input_path, FLAGS.filename_y)
        to_pd_fth(FLAGS.output_path, FLAGS.filename_y, df_y)

    to_pd_fth(FLAGS.output_path, FLAGS.filename_x, x)
    to_pckl(FLAGS.output_path, pca_object_name, pca_obj)


if __name__ == '__main__':
    app.run(main)

import os
from unittest import TestCase
import numpy as np
from keras_transformer_xl import load_trained_model_from_checkpoint


class TestLoader(TestCase):

    def test_load_test(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        checkpoint_path = os.path.join(current_path, 'test_checkpoint')
        model = load_trained_model_from_checkpoint(
            config_path=os.path.join(checkpoint_path, 'config.json'),
            checkpoint_path=os.path.join(checkpoint_path, 'model.ckpt')
        )
        model.summary()
        tokens = np.load(os.path.join(checkpoint_path, 'tokens.npy'))
        memory_0 = np.load(os.path.join(checkpoint_path, 'memory_0.npy'))
        memory_1 = np.load(os.path.join(checkpoint_path, 'memory_1.npy'))
        softmax = np.load(os.path.join(checkpoint_path, 'softmax.npy'))
        new_memory_0 = np.load(os.path.join(checkpoint_path, 'new_memory_0.npy'))
        new_memory_1 = np.load(os.path.join(checkpoint_path, 'new_memory_1.npy'))
        positions = np.expand_dims(np.arange(tokens.shape[1] + memory_0.shape[1] - 1, -1, -1), axis=0)
        outputs = model.predict([tokens, positions, memory_0, memory_1])
        self.assertTrue(np.allclose(new_memory_0[0, 10:], outputs[1]))
        self.assertTrue(np.allclose(new_memory_1[0, 10:], outputs[2], atol=1e-6))
        self.assertTrue(np.allclose(softmax, outputs[0]))
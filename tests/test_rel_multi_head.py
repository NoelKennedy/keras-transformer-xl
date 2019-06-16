from unittest import TestCase
import numpy as np
from keras_transformer_xl.backend import keras
from keras_transformer_xl.backend import backend as K
from keras_transformer_xl import RelativeBias, RelativePartialMultiHeadSelfAttention


class TestRelMultiHead(TestCase):

    def test_sample(self):
        inputs = np.array([
            [
                [0.7562695145606995, -0.7532438039779663, -0.2882295846939087, -1.6990371942520142],
                [-0.36805298924446106, 1.1673600673675537, -0.6914459466934204, -0.764503002166748],
                [-0.8440324068069458, 0.05585795268416405, -0.5827732086181641, 1.5028537511825562],
            ],
            [
                [-0.09864164888858795, -0.5235034227371216, -1.6001530885696411, 0.034417327493429184],
                [2.043482780456543, -0.27436429262161255, 0.04834289103746414, -1.0368596315383911],
                [-0.09311037510633469, 1.366316556930542, -0.38340920209884644, -1.2647643089294434],
            ],
        ])
        relatives = np.array([
            [
                [1.521276831626892, -0.7854311466217041, -0.467421293258667, -1.0460200309753418],
                [0.3705556094646454, -0.12273261696100235, 1.8138707876205444, -0.26957085728645325],
                [-0.15162771940231323, -0.19654664397239685, -1.7793004512786865, -0.6987102031707764],
            ],
            [
                [1.521276831626892, -0.7854311466217041, -0.467421293258667, -1.0460200309753418],
                [0.3705556094646454, -0.12273261696100235, 1.8138707876205444, -0.26957085728645325],
                [-0.15162771940231323, -0.19654664397239685, -1.7793004512786865, -0.6987102031707764],
            ],
        ])
        memories = np.zeros((2, 0, 4))

        kernel_q = np.array([
            [0.32681036318004547, -1.1363779747587972, 1.2424950830966563, 0.613169803410901],
            [0.19156716698736181, -0.15233131547247872, -0.16130616338419873, -1.5391239758406403],
            [0.8386004334587568, 0.158423477487577, -1.6298737099566283, -1.2476893436624792],
            [-1.8390076172747616, -0.6984487776859649, 1.7229575808498785, -0.05514513857644962],
        ])
        kernel_k = np.array([
            [-0.5537408608863357, -0.4086071455923046, -0.13042129128885002, 0.7326026846217363],
            [-0.9965187549427492, -0.7286151488450243, -1.4269400640112133, 0.12752591749386982],
            [-0.6842234254089083, 1.2938629380821804, -0.713571658756806, 0.7387086112901271],
            [-1.2420165307152238, 0.7450912596769113, -0.5036154349645774, -1.4161019970745967],
        ])
        kernel_v = np.array([
            [-0.6396944907214142, 1.22301664512685, -0.9673069099782774, 0.6593494357199338],
            [-2.0010110577965783, -0.024541032664251092, 0.6614265651081772, -0.06233478795012013],
            [0.5843029435066284, -0.27128167541306714, -1.165650716838653, 0.3394579881849406],
            [-0.4033331631189724, 1.910258142043872, -0.5085143504562967, 0.05894554241531747],
        ])
        kernel_kv = np.concatenate([kernel_k, kernel_v], axis=-1)
        kernel_o = np.array([
            [1.0015451559801243, -0.41965070720383035, -0.6800689195006436, -1.3119449289237803],
            [0.7487130375684998, -0.2875756074838825, -0.39454047242128376, 1.5645034642903253],
            [-0.4244371286817957, 1.8712603426351773, 0.5442439581019961, 1.3203132828621442],
            [-0.45182923128222996, 2.531083895835167, -0.21672610899025968, 1.7673879116655695],
        ])
        kernel_r = np.array([
            [-0.8817194029613362, -0.47497798682688624, -0.531267085230172, 0.43338928943049837],
            [-0.6655645822150862, 1.0109350638555383, 0.12862169808408846, 0.2660771849859784],
            [0.2341787847442309, -0.5514102704837403, 0.18339345878624577, 1.4227633495535283],
            [-0.7641095447924122, -0.1450007600387442, 1.5279135983387981, -0.5072818940455809],
        ])

        bias_context = np.array([0.35799413043562894, -0.15005629449852656, 0.6263946579941496, 0.3409731658714878])
        bias_relative = np.array([-0.3082491589087075, -0.3751562822576601, 0.26067868083146517, 1.1346146882950412])

        input_layers = [
            keras.layers.Input(shape=(3, 4), name='Inputs'),
            keras.layers.Input(shape=(3, 4), name='Relatives'),
            keras.layers.Input(shape=(None, 4), name='Memories'),
        ]
        bias_layer = RelativeBias(
            4,
            name='Bias')
        att_layer = RelativePartialMultiHeadSelfAttention(
            4, 2,
            use_bias=False,
            name='Attention')
        outputs = [att_layer(input_layers + bias_layer(inputs[0]))]
        bias_layer.set_weights([bias_context, bias_relative])
        att_layer.set_weights([kernel_q, kernel_kv, kernel_o, kernel_r])
        model = K.function(input_layers, outputs)
        predicted = model([inputs, relatives, memories])[0]
        expected = np.array([
            [
                [-0.2668300271034241, 0.8172217011451721, -0.2616312801837921, -4.925265789031982],
                [-1.2477881908416748, 2.791245222091675, 1.3753974437713623, -2.8643665313720703],
                [-0.05716386437416077, 1.65394926071167, 0.5282477736473083, 4.514030456542969]
            ],
            [
                [0.0369393527507782, 1.3558001518249512, 0.7286960482597351, 1.4957764148712158],
                [0.0372699499130249, 1.3527781963348389, 0.7238105535507202, 1.495449185371399],
                [-1.0944300889968872, 2.2761600017547607, 1.4323406219482422, 1.7387018203735352],
            ],
        ])
        self.assertEqual((2, 3, 4), predicted.shape)
        self.assertTrue(np.all(np.abs(predicted - expected) < 1e-4))
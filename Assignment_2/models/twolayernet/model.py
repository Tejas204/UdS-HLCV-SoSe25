import numpy as np
from abc import abstractmethod


class TwoLayerNetv1(object):
    """
    A two-layer fully-connected neural network. The net has an input dimension of
    N, a hidden layer dimension of H, and performs classification over C classes.
    We train the network with a softmax loss function and L2 regularization on the
    weight matrices. The network uses a ReLU nonlinearity after the first fully
    connected layer.

    In other words, the network has the following architecture:

    input - fully connected layer - ReLU - fully connected layer - softmax

    The outputs of the second fully-connected layer are the scores for each class.
    """

    def __init__(self, input_size, hidden_size, output_size, std=1e-4):
        """
        Initialize the model. Weights are initialized to small random values and
        biases are initialized to zero. Weights and biases are stored in the
        variable self.params, which is a dictionary with the following keys:

        W1: First layer weights; has shape (D, H)
        b1: First layer biases; has shape (H,)
        W2: Second layer weights; has shape (H, C)
        b2: Second layer biases; has shape (C,)

        Inputs:
        - input_size: The dimension D of the input data.
        - hidden_size: The number of neurons H in the hidden layer.
        - output_size: The number of classes C.
        """
        np.random.seed(0)
        self.std = std
        self.params = {}
        self.params['W1'] = std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)
        
    def forward(self, X):
        """
        Compute the final outputs for a two layer fully connected neural
        network.

        Inputs:
        - X: Input data of shape (N, D). Each X[i] is a training sample.
        - y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
          an integer in the range 0 <= y[i] < C. This parameter is optional; if it
          is not passed then we only return scores, and if it is passed then we
          instead return the loss and gradients.
        - reg: Regularization strength.

        Returns:
        A matrix scores of shape (N, C) where scores[i, c] is
        the score for class c on input X[i].
        """
        # Unpack variables from the params dictionary
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        N, D = X.shape

        # Compute the forward pass
        softmax_scores = None
        #############################################################################
        # TODO: Perform the forward pass, computing the class probabilities for the #
        # input. Store the result in the scores variable, which should be an array  #
        # of shape (N, C).                                                          #
        #############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        

        # Define dot product of weights and inputs
        dot_product_l1 = np.dot(X, W1)

        # Calculate z_2 := dot_product_l1 + bias
        z_2 = np.add(dot_product_l1, b1)

        # Use activation function for z_2
        # relu_non_linear_activation = lambda x: 0 if x < 0 else x
        for row in range(z_2.shape[0]):
            for column in range(z_2.shape[1]):
                if z_2[row][column] < 0:
                    z_2[row][column] = 0
                else:
                    continue
                
        # Determine a2 for future calculations
        a_2 = z_2

        # Calculate the dot product of the second layer
        dot_product_l2 = np.dot(z_2, W2)

        # Calculate z_3 := dot_product_l2 + bias
        z_3 = np.add(dot_product_l2, b2)

        # Apply softmax activation
        sum_exponent = 0
        # softmax_scores = np.empty_like(z_3)
        
        for row in range(z_3.shape[0]):
            sum_exponent = 0
            for column in range(z_3.shape[1]):
                sum_exponent += np.exp(z_3[row][column])
                if sum_exponent == 0:
                    sum_exponent = self.std
            
            for column in range(z_3.shape[1]):
                z_3[row][column] = np.exp(z_3[row][column]) / sum_exponent
            
        softmax_scores = z_3
        
        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # If the targets are not given then jump out, we're done
        return softmax_scores, a_2
    
    @abstractmethod
    def compute_loss(self, **kwargs):
        raise NotImplementedError


class TwoLayerNetv2(TwoLayerNetv1):
    
    def compute_loss(self, X, y=None, reg=0.0):
        """
        Compute the loss and gradients for a two layer fully connected neural
        network.

        Inputs:
        - X: Input data of shape (N, D). Each X[i] is a training sample.
        - y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
          an integer in the range 0 <= y[i] < C. This parameter is optional; if it
          is not passed then we only return scores, and if it is passed then we
          instead return the loss and gradients.
        - reg: Regularization strength.

        Returns:
        - loss: Loss (data loss and regularization loss) for this batch of training
          samples.
        """
        # Unpack variables from the params dictionary
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        N, D = X.shape

        # Compute the forward pass
        softmax_scores = None
        #############################################################################
        # TODO: Perform the forward pass, computing the class probabilities for the   #
        # input. Store the result in the scores variable, which should be an array    #
        # of shape (N, C).                                                            #
        # Note that you don't need to re-implement the forward pass here. This class  #
        # inherits the v1 class implemented above. Thus you can simply use the method #
        # from the parent (i.e v1) class.                                             #
        #############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # Calculate the softmax scores for each element
        softmax_scores, a_2 = TwoLayerNetv1.forward(self, X=X)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # If the targets are not given then jump out, we're done
        if y is None:
            return softmax_scores

        # Compute the loss
        loss = 0.
        #############################################################################
        # TODO: Finish the forward pass, and compute the loss. This should include  #
        # both the data loss and L2 regularization for W1 and W2. Store the result  #
        # in the variable loss, which should be a scalar. Use the Softmax           #
        # classifier loss.                                                          #
        #############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        
        # Calculate average loss
        summation = 0
        for row in range(softmax_scores.shape[0]):
            # Calculate the sum of exponents for each input
            sum_exponent = np.sum(softmax_scores[row])

            # Determine the softmax probability of the correct class label
            # y stores all the correct classes, which can be used as indices
            # So, if y_2 = 1 => for the 2nd input, the correct class is at index 1
            exponent_label = softmax_scores[row][y[row]]
            summation += -np.log(exponent_label / sum_exponent)
        
        # Calculate regularization term 1 and 2
        flattened_weights_1 = W1.flatten()
        flattened_weights_2 = W2.flatten()
  
        norm_weights_1 = sum([weight**2 for weight in flattened_weights_1])
        norm_weights_2 = sum([weight**2 for weight in flattened_weights_2])

        regularization_term = reg * (norm_weights_1 + norm_weights_2)

        # Final loss
        loss = (summation / softmax_scores.shape[0]) + regularization_term
        # print("Calculated loss is: " + str(loss))

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        return loss
    
    @abstractmethod
    def back_propagation(self, **kwargs):
        raise NotImplementedError # No need to implement here!
    

class TwoLayerNetv3(TwoLayerNetv2):
    
    def back_propagation(self, X, y=None, reg=0.0):
        """
        Compute the loss and gradients for a two layer fully connected neural
        network.

        Inputs:
        - X: Input data of shape (N, D). Each X[i] is a training sample.
        - y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
          an integer in the range 0 <= y[i] < C. This parameter is optional; if it
          is not passed then we only return scores, and if it is passed then we
          instead return the loss and gradients.
        - reg: Regularization strength.

        Returns:
        - loss: Loss (data loss and regularization loss) for this batch of training
          samples.
        - grads: Dictionary mapping parameter names to gradients of those parameters
          with respect to the loss function; has the same keys as self.params.
        """
        # Unpack variables from the params dictionary
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        N, D = X.shape


        # Compute the forward pass
        scores = 0.
        #############################################################################
        # TODO: Perform the forward pass, computing the class probabilities for the   #
        # input. Store the result in the scores variable, which should be an array    #
        # of shape (N, C).                                                            #
        #                                                                             #
        # Note that you don't need to re-implement the forward pass here. This class  #
        # inherits the v2 (thus also v1) class implemented above.                     #
        # Thus you can simply use the method from the parent class.                   #
        #############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)****

        # Calculate the softmax scores for each element
        scores, a_2 = TwoLayerNetv2.forward(self, X=X)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # If the targets are not given then jump out, we're done
        if y is None:
            return scores

        # Compute the loss
        loss = 0.
        #############################################################################
        # TODO: Finish the forward pass, and compute the loss. This should include    #
        # both the data loss and L2 regularization for W1 and W2. Store the result    #
        # in the variable loss, which should be a scalar. Use the Softmax             #
        # classifier loss.                                                            #
        # Note that you don't need to re-implement the forward pass here. This class  #
        # inherits the v2 class implemented above. Thus you can simply use the method #
        # from the parent (i.e v2) class.                                             #
        #############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        #  Compute the loss of the gradient
        loss = TwoLayerNetv2.compute_loss(self, X=X, y=y, reg=reg)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # Backward pass: compute gradients
        grads = {}
        #############################################################################
        # TODO: Compute the backward pass, computing the derivatives of the weights #
        # and biases. Store the results in the grads dictionary. For example,       #
        # grads['W1'] should store the gradient on W1, and be a matrix of same size #
        #############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        ####### Preliminaries #######
        # Construct delta
        delta = np.empty_like(scores)

        for row in range(scores.shape[0]):
            for column in range(scores.shape[1]):
                if column == y[row]:
                    delta[row][column] = 1
                else:
                    delta[row][column] = 0
        
        ####### Gradient of loss function w.r.t z_3 #######
        # Compute the gradient of the loss function
        loss_gradient = (np.subtract(scores, delta)) / N


        ####### Derivatives #######

        # Calculate the derivative of J with respect to W2
        grads['W2'] = np.dot(a_2.T, loss_gradient) + 2 * np.multiply(W2, reg)

        # Calculate the derivative of J with respect to B2
        scores = scores - delta
        grads['b2'] = np.sum(scores / N, axis=0)

        # Calculate the derivative of J with respect to W1
        d_z3 = np.dot(scores/N, np.transpose(W2))
        d_relu = np.zeros(a_2.shape)
        for row in range(a_2.shape[0]):
            for column in range(a_2.shape[1]):
                if a_2[row][column] != 0:
                    d_relu[row][column] = 1

        one_hot_encoded = np.multiply(d_z3, d_relu)        
        grads['W1'] = np.dot(np.transpose(X), one_hot_encoded) + (2 * reg * W1)

        # Calculate the derivative of J with respect to B1
        grads['b1'] = np.sum(one_hot_encoded, axis=0)
                    

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        return loss, grads
    
    @abstractmethod
    def train(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def predict(self, **kwargs):
        raise NotImplementedError
    

class TwoLayerNetv4(TwoLayerNetv3):
    
    def train(self, X, y, X_val, y_val,
              learning_rate=1e-3, learning_rate_decay=0.95,
              reg=5e-6, num_iters=100,
              batch_size=200, verbose=False):
        """
        Train this neural network using stochastic gradient descent.

        Inputs:
        - X: A numpy array of shape (N, D) giving training data.
        - y: A numpy array f shape (N,) giving training labels; y[i] = c means that
          X[i] has label c, where 0 <= c < C.
        - X_val: A numpy array of shape (N_val, D) giving validation data.
        - y_val: A numpy array of shape (N_val,) giving validation labels.
        - learning_rate: Scalar giving learning rate for optimization.
        - learning_rate_decay: Scalar giving factor used to decay the learning rate
          after each epoch.
        - reg: Scalar giving regularization strength.
        - num_iters: Number of steps to take when optimizing.
        - batch_size: Number of training examples to use per step.
        - verbose: boolean; if true print progress during optimization.
        """
        num_train = X.shape[0]
        iterations_per_epoch = max(num_train / batch_size, 1)

        # Use SGD to optimize the parameters in self.model
        loss_history = []
        train_acc_history = []
        val_acc_history = []

        for it in range(num_iters):
            X_batch = X
            y_batch = y

            #########################################################################
            # Create a random minibatch of training data and labels, storing        #
            # them in X_batch and y_batch respectively.                             #
            #########################################################################
            if batch_size > num_train:
                rand_ind = np.random.choice(num_train, size=batch_size, replace=True)
            else:
                rand_ind = np.random.choice(num_train, size=batch_size, replace=False)
            X_batch = X[rand_ind]
            y_batch = y[rand_ind]
            #########################################################################
            

            # Compute loss and gradients using the current minibatch
            loss, grads = self.back_propagation(X_batch, y=y_batch, reg=reg)
            loss_history.append(loss)

            #########################################################################
            # TODO: Use the gradients in the grads dictionary to update the         #
            # parameters of the network (stored in the dictionary self.params)      #
            # using stochastic gradient descent. You'll need to use the gradients   #
            # stored in the grads dictionary defined above.                         #
            # Do not forget to apply the learning_rate                              #
            #########################################################################
            # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

            for params in self.params:
                self.params[params] -= learning_rate * grads[params]
            # v_W1 = -learning_rate * grads['W1']
            # v_W2 = -learning_rate * grads['W2']
            # v_b1 = -learning_rate * grads['b1']
            # v_b2 = -learning_rate * grads['b2']

            # self.params['W1'] = self.params['W1'] + v_W1
            # self.params['W2'] = self.params['W2'] + v_W2
            # self.params['b1'] = self.params['b1'] + v_b1
            # self.params['b2'] = self.params['b2'] + v_b2



            # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

            if verbose and it % 100 == 0:
                print(f'iteration {it} / {num_iters}: loss {loss}', end='\r')

            # Every epoch, check train and val accuracy and decay learning rate.
            if it % iterations_per_epoch == 0:
                # Check accuracy
                train_acc = (self.predict(X_batch) == y_batch).mean()
                val_acc = (self.predict(X_val) == y_val).mean()
                train_acc_history.append(train_acc)
                val_acc_history.append(val_acc)

                # Decay learning rate
                learning_rate *= learning_rate_decay

        return {
          'loss_history': loss_history,
          'train_acc_history': train_acc_history,
          'val_acc_history': val_acc_history,
        }
    
    def predict(self, X):
        """
        Use the trained weights of this two-layer network to predict labels for
        data points. For each data point we predict scores for each of the C
        classes, and assign each data point to the class with the highest score.

        Inputs:
        - X: A numpy array of shape (N, D) giving N D-dimensional data points to
          classify.

        Returns:
        - y_pred: A numpy array of shape (N,) giving predicted labels for each of
          the elements of X. For all i, y_pred[i] = c means that X[i] is predicted
          to have class c, where 0 <= c < C.
        """
        y_pred = None

        ###########################################################################
        # TODO: Implement this function; it should be VERY simple!                #
        ###########################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        
        scores, a_2 = self.forward(X)

        y_pred = np.argmax(scores, axis=1)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        return y_pred
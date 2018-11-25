
import numpy as np

def data_loader(filename):

    """
    loads data from 'filename', and then returns a tuple of (X, y) to
    be used in Regression
    """

    with open(filename, "r") as file:
        data = np.genfromtxt(file, comments="#")
    return (data[:, :-1], data[:, -1:])

class Regression:

    def __init__(self, X, y, lamb, rho):
        
        """
        y is y values from a dataset, stored in a 2-D array, y[i] having just
        one element y_i for each data. X is x values from the dataset stored
        in a 2-D array, X[i] storing x_1, x_2, ..., x_n for each data. 1 is
        inserted at the beginning of each data for the constant term.
        """

        self.y = y
        self.X = np.insert(X, 0, 1., axis=1)
        self.lamb, self.rho = lamb, rho
        self.beta = np.array([self.y[0] / x for x in self.X[0]]).reshape(len(self.X[0]), 1)
        self.theta = self.beta[:]
        self.mu = np.zeros((len(self.X[0]), 1), dtype='float64')
        self.num_data = len(self.y)
        self.num_parameters = len(self.X[0])

    def run(self, epochs):

        """
        runs update() 'epochs' times
        """

        for epoch in range(epochs):
            self.update()
            print("epoch {}: SSE = {}, error = {}".format(epoch, self.sse(), self.error()))

    def update(self):

        """
        updates β_(t+1), θ_(t+1), μ_(t+1) from β_t, θ_t, μ_t
        """

        self.beta = np.dot(np.linalg.inv(np.dot(np.transpose(self.X), self.X) + self.rho * np.eye(self.num_parameters)),
                           np.dot(np.transpose(self.X), self.y) + self.rho * self.theta - self.mu)
        self.theta = np.array([soft_threshold(self.lamb / self.rho, self.beta[i] + self.mu[i] / self.rho)
                               for i in range(self.num_parameters)])
        self.mu = self.mu + self.rho * (self.beta - self.theta)

    def error(self):

        """
        the function that is supposed to be minimized
        """

        m = self.y - np.dot(self.X, self.beta)
        return (1/2) * np.sqrt(np.sum(m * m)) + self.lamb * np.sum(abs(self.theta[1:]))

    def sse(self):

        """
        the square root of the sum of squared errors
        """

        m = self.y - np.dot(self.X, self.beta)
        return (1/2) * np.sqrt(np.sum(m * m))

    def primitive_sse(self):

        """
        the square root of the sum of squared errors, if y_hat were just the average
        of all y values. can be used to evaluate whether the regression has produced
        a meaningful result
        """

        m = self.y - np.full((self.num_data, 1), np.sum(self.y) / self.num_data)
        return (1/2) * np.sqrt(np.sum(m * m))

def soft_threshold(tau, z):
    return np.sign(z) * max((abs(z) - tau), 0)
# from time import sleep
def PIDcontroller(error):
    """
    error = desired_value - actual_value
    """
    error_prior = 0
    integral_prior = 0
    KP = 0.1
    KI = 1e-5
    KD = 0.1
    bias = 0.5 #when KP*error + KI*integral + KD*derivative = 0, in order not to stop the motion
    iteration_time = 3 # intervals between iterations

    while True:
        # integral term
        integral = integral_prior + error
        # or integral = integral_prior + error*iteration_time

        # derivative term
        derivative = error-error_prior
        # or derivative = (error-error_prior)/iteration_time

        # summation of the three terms
        output = KP*error + KI*integral + KD*derivative + bias

        # update the prior values in the next iteration with current values
        error_prior = error
        integral_prior = integral

        # uncomment this method if you want to put intervals between iterations
        # sleep(iteration_time)
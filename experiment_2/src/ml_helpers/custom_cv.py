import numpy as np

class BlockingTimeSeriesSplit():
    ''' Note that this might still have an error: it does not exhaust all examples'''
    
    # Source: https://hub.packtpub.com/cross-validation-strategies-for-time-series-forecasting-tutorial/
    def __init__(self, n_splits):
        self.n_splits = n_splits
    
    def get_n_splits(self, X, y, groups):
        return self.n_splits
    
    def split(self, X, y=None, groups=None):
        n_samples = len(X)
        k_fold_size = n_samples // self.n_splits  # Number of samples per fold
        indices = np.arange(n_samples)

        margin = 0
        for i in range(self.n_splits):
            start = i * k_fold_size                  # Repeats every [k_fold_size] samples
            stop = start + k_fold_size               # Spans [k_fold_size] samples
            mid = int(0.8 * (stop - start)) + start  # Determines the split within the fold (80-20)
            #print(k_fold_size, self.n_splits, i, start,stop,mid)
            yield indices[start: mid], indices[mid + margin: stop]
            
class GroupedBlockingTimeSeriesSplit():
    def __init__(self, n_splits):
        self.n_splits = n_splits
    
    #def get_n_splits(self, X, y, X):
    #    return self.n_splits
    
    def split(self, X, y=None, groups=None, n_samples_per_group=None):
        n_samples = len(X)
        k_fold_size = (n_samples//n_samples_per_group) // self.n_splits # Number of groups per fold
        overflow = (n_samples//n_samples_per_group) % (self.n_splits) # Number of groups per fold
        indices = np.arange(n_samples)

        margin = 0
        for i in range(self.n_splits):
            start = i * (k_fold_size*n_samples_per_group)
            stop = start + (k_fold_size*n_samples_per_group)
            mid = int(0.8 * (k_fold_size))*n_samples_per_group + start
            
            if i<overflow:
                start += i*n_samples_per_group
                mid += (1+i)*n_samples_per_group
                stop += (1+i)*n_samples_per_group
            else:
                start += (overflow)*n_samples_per_group
                mid += (overflow)*n_samples_per_group
                stop += (overflow)*n_samples_per_group
                
            yield indices[start: mid], indices[mid + margin: stop]
            
            
class GroupedTimeSeriesSplit():
    ''' Note that this this might still: it does not exhaust all examples'''
    def __init__(self, n_splits):
        self.n_splits = n_splits
    
    #def get_n_splits(self, X, y, X):
    #    return self.n_splits
    
    def split(self, X, y=None, groups=None, n_samples_per_group=None):
        n_samples = len(X)
        k_fold_size = (n_samples//n_samples_per_group) // (self.n_splits+1) # Number of groups per fold
        overflow = (n_samples//n_samples_per_group) % (self.n_splits+1)    # Number of groups per fold
        indices = np.arange(n_samples)

        margin = 0
        start = (k_fold_size*n_samples_per_group)
        if overflow>0:
            start += n_samples_per_group*overflow
        for i in range(self.n_splits):                
            stop = start + (k_fold_size*n_samples_per_group)
            yield indices[0: start], indices[start: stop]
            start = stop
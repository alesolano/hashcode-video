#
# Google Hash Code 2017 - Qualification Round
#
# Copyright (c) 2017 Team "Makineo"
#
# Version 1.0
#

import numpy as np
import sys

def read_file(filename):
    
    with open(filename, 'r') as f:
        line = f.readline()
        V, E, R, C, X = [int(n) for n in line.split()]
        
        line = f.readline()
        v_sizes = []
        for n in line.split():
            v_sizes.append(int(n))
            
        requests_per_video = np.zeros([1, V])
        
        endpoints = [] # lista de instancias a la clase Endpoint
        for endpoint in range(E):
            line = f.readline()
            dc_lat, num_caches = [int(n) for n in line.split()]
            
            cache_lats = np.zeros([1, C]) # habia fallo: tenia np.zeros([1, E])
            
            for cache in range(num_caches):
                line = f.readline()
                c_index, c_lat = [int(n) for n in line.split()]
                cache_lats[0][c_index] = c_lat
                
            new_ep = Endpoint(dc_lat, cache_lats, requests_per_video) # new instance of class Endpoint
            endpoints.append(new_ep)
        
        for request in range(R):
            line = f.readline()
            vid_index, ep_index, num_req = [int(n) for n in line.split()]
            endpoints[ep_index].requests_per_video[0][vid_index] += num_req 
            
        caches = []
        videos = np.zeros([1, V])
        for cache_index in range(C):
            new_cache = Cache(cache_index, videos, X)
            caches.append(new_cache)
        
        return v_sizes, endpoints, caches


class Endpoint():
    
    def __init__(self, dc_lat, cache_lats, requests_per_video):
        self.dc_lat = dc_lat
        self.cache_lats = np.copy(cache_lats)
        self.requests_per_video = np.copy(requests_per_video) # array de longitud V
        
        self.savings = dc_lat - cache_lats # ahorro si cojo esa cache
    
    def get_most_popular(self):
        self.popular = self.requests_per_video.argmax() # most popular video
        

class Cache():
    
    def __init__(self, index, videos, space):
        self.index = index
        self.savings = np.copy(videos)
        self.space_left = space
        self.videos_stored = []
    
    def get_savings_by_video(self, endpoints):
        for ep in endpoints:
            #ep.get_most_popular()
            if ep.cache_lats[0][self.index] != 0: #if connection exists
                self.savings[0][ep.popular] += ep.requests_per_video[0][ep.popular] * ep.savings[0][self.index]
    
    def store_videos(self, vid_sizes):
        vid_seen = 0
        while (self.space_left > 0) and (vid_seen < len(vid_sizes)):
            best_video = self.savings.argmax()
            if vid_sizes[best_video] <= self.space_left:
                self.space_left -= vid_sizes[best_video]
                self.savings[0][best_video] = -1
                self.videos_stored.append(best_video)
                print("Space left in cache %d: %d" % (self.index, self.space_left))
            vid_seen += 1
        print("Videos stored by cache {}: {}".format(self.index, self.videos_stored))


def write_file(caches, filename):
    '''
    Write the output file
    '''
    with open(filename, 'w') as f:
        f.write('{}\n'.format(len(caches)))
        for cache in caches:
            f.write('%d ' % cache.index)
            f.write(' '.join([str(item) for item in cache.videos_stored]) + '\n')

def main():
    '''
    Main function
    '''
    if len(sys.argv) < 3:
        sys.exit('Syntax: %s <filename> <output>' % sys.argv[0])

    print('Running on file %s' % sys.argv[1])
    
    vid_sizes, endpoints, caches = read_file(sys.argv[1])
    
    for ep in endpoints:
        ep.get_most_popular()
    for cache in caches:
        cache.get_savings_by_video(endpoints)
        cache.store_videos(vid_sizes)
        
    write_file(caches, sys.argv[2])


if __name__ == '__main__':
    main()


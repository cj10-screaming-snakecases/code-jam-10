
##pip install git+https://github.com/martinResearch/PyIPOL.git
##pip install cython
##pip install imageio
##pip install matplotlib
##pip install argparse
##pip install opencv-python
##pip install wrapper
##pip install barcodenumber
#import argparse
#import numpy as np
#from imageio import imread, imwrite
#import matplotlib.pyplot as plt
#import cv2
#import wrapper
#
## Import the denoising algorithm wrappers
#import ipol.wrappers.Implementation_of_the_Non_Local_Bayes_Image_Denoising_Algorithm as nl_bayes_wrapper
#import ipol.wrappers.DCT_Image_Denoising_a_Simple_and_Effective_Image_Denoising_Algorithm as dct_wrapper
#import ipol.wrappers.Non_Local_Means_Denoising as nl_means_wrapper
#import ipol.wrappers.Rudin_Osher_Fatemi_Total_Variation_Denoising_using_Split_Bregman as tv_denoise_wrapper
#
#def apply_denoising_algorithm(image, algorithm, sigma):
#    if algorithm == "NLBayes":
#        return nl_bayes_wrapper.NL_Bayes(image, sigma=sigma)
#    elif algorithm == "DCT":
#        return dct_wrapper.DCTdenoising(image, sigma=sigma)
#    elif algorithm == "NLMeans":
#        return nl_means_wrapper.nlmeans(image, sigma)
#    elif algorithm == "TVDenoise":
#        return tv_denoise_wrapper.tvdenoise(image, model='gaussian', sigma=sigma)
#    else:
#        raise ValueError("Invalid denoising algorithm selected.")
#
#def main():
#    parser = argparse.ArgumentParser(description="Apply denoising algorithms to an input image.")
#    parser.add_argument("input_image", type=str, help="Path to the input noisy image.")
#    parser.add_argument("output_image", type=str, help="Path to save the denoised output image.")
#    parser.add_argument("--algorithm", choices=["NLBayes", "DCT", "NLMeans", "TVDenoise"], required=True, help="Select denoising algorithm.")
#    parser.add_argument("--sigma", type=float, required=True, help="Noise standard deviation for the selected algorithm.")
#    
#    args = parser.parse_args()
#    
#    
#    noisy_image = imread(args.input_image)
#    
#    
#    denoised_image = apply_denoising_algorithm(noisy_image, args.algorithm, args.sigma)
#    
#    
#    imwrite(args.output_image, denoised_image)
#    
#    #Display 
#    plt.subplot(1, 3, 1)
#    plt.imshow(noisy_image, cmap='gray')
#    plt.title("Noisy Image")
#    
#    plt.subplot(1, 3, 2)
#    plt.imshow(denoised_image, cmap='gray')
#    plt.title("Denoised Image")
#    
#    plt.subplot(1, 3, 3)
#    plt.imshow(np.abs(denoised_image.astype(np.float) - noisy_image.astype(np.float)) / 5, cmap='gray')
#    plt.title("Difference (scaled)")
#    
#    plt.show()
#
#if __name__ == '__main__':
#    main()
#

# Pylmonary Embolism API

This repository contains an API for the prediction of Pulmonary Embolism (PE) from a zip of DICOM images.

<br>
<p align="center">
    <img src="../img/grad_cam.gif"/>
</p>
<br>

## Table of Contents
0. [Introduction](#introduction)
0. [Model](#model)
0. [Usage](#usage)

## Introduction

Pulmonary embolism (PE) is a serious and potentially life-threatening condition that represents the third most common cause of cardiovascular-related deaths. Establishing a diagnosis of PE can be challenging, as patients often present with nonspecific symptoms. Classic presentations include acute onset of dyspnea, pleuritic chest pain, tachycardia, and signs of right heart strain. Prompt and accurate detection of PE and an assessment of its severity are critical to guiding patient treatment. In addition, it is important to avoid overdiagnosis, as the treatment of PE carries its own set of risks.   

CT pulmonary angiography (CTPA) is the preferred and most frequently used imaging modality to evaluate patients suspected of having PE. CTPA studies consist of hundreds of images that require detailed radiologist review to identify filling defects within the pulmonary arterial vasculature. Given the number of images that require scrutiny and increased use of CTPA and imaging in general, the constraint on radiologists’ time may contribute to delays in diagnosis.   


## Model 

[The PENet repository](https://github.com/marshuang80/penet) contains the code and the model (PENet) described in the [paper](https://rdcu.be/b3Lll) *"PENet: A Scalable Deep-learning model for Automated Diagnosis of Pulmonary Embolism Using Volumetric CT Scan"* published on Nature Digital Medicine. 

#### Download trained weights

The checkpoints and weights for PENet are stored [here](https://stanfordmedicine.box.com/s/uql0ikebseltkkntiwl5rrn6zzuww6jt). 

⚠️ If it's not already present in the data folder, please download and place it there.


## Usage

#### Environment Setup 
1. Please install [Docker](https://docs.docker.com/get-docker/) in order to create a Docker environment.
2. Clone this repo (from the command-line: `git clone git@github.com:Gladouu/Pulmonary-Embolism.git`).
3. You must be in the API folder : `cd Pulmonary_Embolism/API`.
4. Create and activate the API from docker-cli : `docker-compose up`.


#### Testing

##### Download the data
In order to test this application, you must have CTPA in DICOM format. If you want, it's possible to find some in open-source, like the FUMPE dataset available [here](https://www.kaggle.com/datasets/andrewmvd/pulmonary-embolism-in-ct-images). 

This is only a suggestion but this dataset will allow you to have the original DICOM and Ground Truth, to visualize the Pulmonary Embolism. We suggest the [ITK-Snap](http://www.itksnap.org/pmwiki/pmwiki.php?n=Main.HomePage) visualization software. You just have to drag and drop the DICOM images, as well as the segmentation (you should select load as main segmentation for overlap).

##### Preprocessing the data
For testing this API, you have to create a zip file from your DICOM images. 

##### Testing
The API is available on your favorite browser at : [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



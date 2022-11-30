
# Introduction
Gathering all the literature on shoulder kinematics, and scapulo-humeral rhythm
With this repository, We aim to gather all the literature on shoulder kinematics, and scapulo-humeral rhythm.
We will try to keep it updated as much as possible. If you have any suggestions, please let us know.


# Table of Contents
[The dataset columns](#The-dataset-columns)
 - [Metadata](##Metadata)
    - [article_title](###article_title)
    - [authors](###authors)
    - [year](###year)
    - [journal](###journal)
- [Experimental conditions](##Experimental-conditions)
    - [invivo](###invivo)
    - [experimental means](###experimental-means)
    - [nb_shoulders](###nb_shoulders)
    - [type_of_movement](###type_of_movement)
    - [posture](###posture)
- [Generic segment columns](##Generic-segment-columns)
    - [XXX_is_isb](###XXX_is_isb)
    - [XXX_is_correctable](###XXX_is_correctable)
    - [XXX_correction_method](###XXX_correction_method)
    - [XXX_origin](###XXX_origin)
    - [XXX_X, XXX_Y or XXX_Z](###XXX_X,-XXX_Y-or-XXX_Z)
- [Other columns](##Other-columns)
    - [Thoracohumeral_sequence](###Thoracohumeral_sequence)
- [Joint motion columns](##Joint-motion-columns)
    - [joint](###joint)
    - [euler_sequence](###euler_sequence)
    - [origin_translation](###origin_translation)
    - [translation_cs](###translation_cs)
-[Data columns and array of data](##Data-columns-and-array-of-data)
    - [is_data_mean](###is_data_mean)
    - [shoulder_id](###shoulder_id)
    - [source_extraction](###source_extraction)
    - [data_humero_thoracic_elevation](###data_humero_thoracic_elevation)
    - [dof_1st_euler](###dof_1st_euler)
    - [dof_2nd_euler](###dof_2nd_euler)
    - [dof_3rd_euler](###dof_3rd_euler)
    - [data_translation_x](###data_translation_x)
    - [data_translation_y](###data_translation_y)
    - [data_translation_z](###data_translation_z)
    
# The dataset columns
The dataset is a csv file, each row aim to represent a joint movement as a function of the humerothoracic elevation angle.
The columns are the following:

## Metadata

### article_title
variable type: string
The title of the article

### authors
variable type: string
The authors of the article

### year
variable type: integer
The year of publication

### journal
variable type: string
The journal where the article was published

## Experimental conditions

### in vivo
variable type: boolean
True if the article is in vivo, False if it is ex vivo

### experimental means
variable type: string
The experimental means used in the article:
- intra cortical pins
- to be completed ...

### nb shoulders
variable type: integer
The number of shoulders/ subjects in the article, sometimes right and left shoulders are counted as two shoulders

### type of movement
variable type: string
The type of movement:
- Dynamic
- to be completed ...

### posture
variable type: string
The posture of the subject when the data was collected:
- Upright standing
- Upright sitting

## Generic segment columns

This columns are generic for the following key words:
- humerus
- parent : referring to the parent segment of a joint
- child : referring to the child segment of a joint

examples: humerus_is_isb, parent_is_isb, child_is_isb

### XXX_is_isb
variable type: boolean
True if the segment follows the ISB recommendations, False otherwise

### XXX_is_isb_correctable
variable type: boolean
True if the segment coordinates system can be corrected to follow the ISB recommendations, False otherwise

### XXX_correction_method
variable type: string
The method used to correct the segment coordinates system to follow the ISB recommendations:
- to_isb : consisting in switching axis to follow the ISB recommendations
- to_isb_like : consisting in switching axis to follow the ISB recommendations as much as possible
- to_kolz_ac_to_pa : consisting in switching axis from acromio-clavicular joint to posterior aspect of the acromion
- to be completed ...

Note: two methods can be combined, to get back to the ISB recommendations, might be a list of strings at the end of the day

### XXX_origin
variable type: string
The anatomical landmark used as origin for the segment coordinates system:
- acromion
- to be completed ...

### XXX_X, XXX_Y or XXX_Z
variable type: string
X, Y and Z denote the axis of the segment coordinates system. The anatomical direction of the axis:
- +anteroposterior: the axis is pointing anteriorly
- -anteroposterior: the axis is pointing posteriorly
- +mediolateral: the axis is pointing medially
- -mediolateral: the axis is pointing laterally
- +vertical: the axis is pointing superiorly
- -vertical: the axis is pointing inferiorly

This nomenclature/terminology has been chosen because in the case the segement coordinate system doesn't properly follow the ISB recommandations,
the axis can vaguely point in the direction, but not strictly regarding the ISB recommendations.

## Other columns
### Thoracohumeral_sequence
variable type: string
The sequence of the thoracohumeral joint:
- yxy
- zyx
- to be completed ...

## Joint motion columns

### joint
variable type: string
The joint name considered on the row: of the csv file :
- sternoclavicular
- scapulothoracic
- acromioclavicular
- glenohumeral

### euler_sequence
variable type: string
The sequence of the joint:
- yxz: ISB for sternoclavicular, acromioclavicular and scapulothoracic joints when segment follows ISB recommendations)
- yxy: ISB for glenohumeral, thoracohumeral joints when segment doesn't follow ISB recommendations)
- zyx
- to be completed ...

### origin_translation
variable type: string
The anatomical landmark used as origin for the translation:
- to be completed ...

### translation_cs
variable type: string
segment name or joint name. It may refer to the proximal, distal or joint coordinate system

## Data columns and array of data

### is_data_mean
variable type: boolean
True if the data is the mean of the subjects, False otherwise

### shoulder_id
variable type: integer
The id of the shoulder/subject, if the data is not the mean of the subjects

### source_extraction
variable type: string
The source of the data:
- data: the data comes from a data file
- engauged: the data comes from the software Engauge

### data_humero_thoracic_elevation
variable type: array of floats
The humero-thoracic elevation data to describe the shoulder rhythm of the joint, in degrees (to be confirmed)

### dof_1st_euler
variable type: array of floats
The first euler angle of the joint, in degrees (to be confirmed)

### dof_2nd_euler
variable type: array of floats
The second euler angle of the joint, in degrees (to be confirmed)

### dof_3rd_euler
variable type: array of floats
The third euler angle of the joint, in degrees (to be confirmed)

### dof_translation_x
variable type: array of floats
The translation along the x axis of the joint, in mm (to be confirmed)

### dof_translation_y
variable type: array of floats
The translation along the y axis of the joint, in mm (to be confirmed)

### dof_translation_z
variable type: array of floats
The translation along the z axis of the joint, in mm (to be confirmed)








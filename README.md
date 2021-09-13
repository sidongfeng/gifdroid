# GIFdroid: Automated Replay of Visual Bug Reports for Android Apps


<p align="center">
<img src="figures/overview.png" width="90%"/> 
</p><p align="center">The overview of GIFdroid consists of three phases, Keyframe Location, GUI Mapping, Execution Trace generation.<p align="center">


GIFdroid is a light-weight image-processing approach to automatically replay the video (GIF) based bug reports for Android apps. GIFdroid consists of three phases, each of which play a crucial role in accomplishing this functionality. Given that GIFdroid was designed and built with extension in mind, each of these phases and each of the component elements of these phases can be extended or substituted to further the functionality of the pipeline as a whole. The intent of this design choice is to allow researchers and developers to customize GIFdroid for future projects or development use cases.

### Keyframe Location

<div style="color:#0000FF" align="center">
<img src="figures/timeframe.png" width="70%"/> 
<figcaption>Figure 1: An illustration of the Y-Diff similarity scores of consecutive frames in the visual recording.</figcaption>
</div>

Note that GUI rendering takes time, hence many frames in the visual recording are showing the partial rendering process. The goal of this phase is to locate keyframes i.e., states in which GUI are fully rendered in a given visual recording.

Inspired by signal processing, we leverage the image processing techniques to build a perceptual similarity score for consecutive frame comparison based on Y-Difference (or Y-Diff), see Figure 1.
Given the consective frame comparision, we identify the keyframe by locating the steady state, where the consecutive frames are similar for a relatively long duration.

### GUI Mapping
Given the sequence of keyframes in the recording, we map the keyframes extracted to states/GUIs within the GUI transitions graph (UTG), hence to infer the actions.
We design an advanced image similarity metric for GUI mapping that first detects the features within pixels and structures using SSIM and ORB, and then compute a combined similarity value.

### Execution Trace generation
<div style="color:#0000FF" align="center">
<img src="figures/lcs.png" width="70%"/> 
<figcaption>Figure 2: Illustration of the execution trace generation. Index sequence 2,3 indicate two types of defective sequences, i.e., missing {𝐷} and wrong mapping to {𝐵}, respectively.</figcaption>
</div>
After mapping keyframes to the GUIs in the UTG, we need to go one step further to connect these GUIs/states into a trace to replay the bug.
However, this process is challenging due to two reasons. First, the extracted keyframe and mapped GUIs may not be 100% accurate, resulting in a mismatch of the groundtruth trace. For example in Figure 2, {𝐷} is missed in the index sequence 2 and the second keyframe is wrongly mapping to {𝐵} in the index sequence 3. Second, different from the uploaded GIF which may start the recording anytime, the recovered trace in our case must begin from the launch of the app.


In this phase, we first generate all candidate sequences in UTG between the app launch to the last keyframe from GIF. By regarding the extracted keyframes as a sequence, our approach then further extracts the Longest Common Subsequence (LCS) between it and all candidate sequences.
The overflow of our approach can be seen in Algorithm 1 in our paper.






<!--
**gifdroid/gifdroid** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->

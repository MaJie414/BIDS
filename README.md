# BIDS 格式整理使用说明

### 要求文件格式

**stimuli:**	可选文件或文件夹 

**ieeg:**	*.edf*

**anat:**	 *.gz*

**behaviour:**	 *.mat* （文件名中需包含**behaviour**）

**info：**	 *.mat*、*.pdf*

**derivatives:** 	可选文件或文件夹。**可填可不填**



## 运行程序

1. 程序目录下创建 **anatpath.txt**和**targetpath.txt**，并分别在文本文件中写入路径。

   > 通常情况下anatpath 和 targetpath不需改变，以此避免重复性输入路径信息。

   - anatpath： 结构数据的文件路径。

     > anatpath 为nas中share文件夹中的BIDS_anat。

   - targetpath: 数据保存路径。

2. 运行程序BIDS_v7.0

   弹窗如下

   ![image](https://user-images.githubusercontent.com/22385389/62091368-113af280-b2a3-11e9-815d-c37bba2df2f6.png)

   因anatpath 和 targetpath已在文本文件中输入，程序自动读取相关信息。（如路径需要修改点击最后一列的*path* 按键）

   - 点击 *files path* 所在行的*path* 按键，选择包含有被试所有数据的文件路径（程序遍历所有文件夹，提取**.mat** / **.edf** / **.pfd**类型文件）。

   - 输入*Subject ID*， 格式要求 g/s_xxxx(拼音)_123456(6位日期)

     > ID 会与 anatpath中的被试ID进行匹配，如所输ID未能在anatpath中找到，则程序无法运行。
   - 根据实验类型选择*CCEP* 或者 *SEEG*  
   
      选择CCEP的话， 不转存行为数据
      
      选择SEEG，要求每个session每个run有对应的行为文件（一个session一个run下可以有多个行为结果，通过taskname进行区分）

   如果targetpath中包含了该被试ID文件夹，会弹窗提示是否覆盖。如选“是”则删除targetpath中原被试ID的数据，如选“否”则可添加ieeg，其余信息仍会覆写。

   ![image](https://user-images.githubusercontent.com/22385389/62018831-f5761480-b1ee-11e9-96de-ab4b63d48dd5.png)

3. 对实验数据进行第一次整理时（targetpath 目录下未包含*data_description.json*文件）

      弹出json文件编辑器，如下图所示。

      ![image](https://user-images.githubusercontent.com/22385389/62019323-f0b26000-b1f0-11e9-9b57-5cec4909201d.png)

   - add info为增加信息

   - 编辑信息

     选中所需编辑行，双击左键便弹出编辑框，编辑完成后点击下方*ok* 键。

   - 删除信息

     选中所要删除行，双击右键即可删除

   编辑完成后点击*Done*即可

4. 文件分类

      ![image](https://user-images.githubusercontent.com/22385389/62019832-36702800-b1f3-11e9-831a-d7549e3c9e86.png)

      无用数据在*file type*列的下拉框中选择*None*，则该数据不会转存。

      - Stimuli ：如targetpath中不包含*Stimuli*文件夹，则会出现，如已有则不出现该行。（该信息不强制）

      - anat_files:

        根据subID自动选择shanghai或guangzhou对应的json文件。（建议查看程序目录下的jsonfiles中的json文件信息）。

        也可点击*create json*自行编辑

      - seeg_files

        设置对应的session、run、task （run、task可不设置）

      - behaviour_files

        同seeg_files

      - info_files

      - derivative_files

        如需添加freesurfer等文件，点击下方 *+* 按钮，窗口中增加一行

        ![image](https://user-images.githubusercontent.com/22385389/62022443-f9aa2e00-b1fe-11e9-939a-4effecde0157.png)

        点击左侧下拉按钮，如单个文件则选择*select file*，如需添加整个文件夹选择*select folder*， 并在右侧空格中输入标签名，程序会在*derivative*文件夹下以该标签名创建文件夹，并将文件保存在此。

        如存在多余行，请点击右侧*—*键，删除该行。

      所有信息设置完成后，点击*OK*，如无报错则程序开始复制文件，如有报错请根据提示进行修改。

5. 填写ieeg.json

      文件复制完成后，窗口自动关闭。并弹出json 编辑窗口

      ![image](https://user-images.githubusercontent.com/22385389/62022764-565a1880-b200-11e9-9608-f4a9b9aa04f3.png)

窗口首行会标明所写json文件的 session、run、task。

> 因行数较多，可通过鼠标滚轴进行上下调整


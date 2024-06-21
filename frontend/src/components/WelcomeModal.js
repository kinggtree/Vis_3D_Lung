import React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

const WelcomeDialog = ({ isOpen, onRequestClose }) => {
  return (
    <Dialog
      open={isOpen}
      onClose={onRequestClose}
      aria-labelledby="welcome-dialog-title"
      aria-describedby="welcome-dialog-description"
    >
      <DialogTitle id="welcome-dialog-title">使用指南</DialogTitle>
      <DialogContent>
        <DialogContentText id="welcome-dialog-description">
          <Typography variant="body1" gutterBottom>
            Step 1. 在第一个选择框中选择想要查看的病人（对应nii文件名），然后点击“加载病人信息”按钮以获取该病人的肺部3D模型和所有有效的CT层。
          </Typography>
          <Typography variant="body1" gutterBottom>
            Step 2. 信息加载完成后，在接下来的两个CT层选择框中，根据需要选择一个（所有CT层或含有病灶的层），然后点击对应的加载按钮。此时，图片会刷新并显示相应的CT层。
          </Typography>
          <Typography variant="h6" color="error" gutterBottom>
            ！！注意！！
          </Typography>
          <Typography variant="body2" gutterBottom>
            1. CT层的编号从小到大排列，对应的肺部扫描顺序是从下到上。
          </Typography>
          <Typography variant="body2" gutterBottom>
            2. 由于服务器带宽限制，模型加载可能需要一些时间，请耐心等待。
          </Typography>
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onRequestClose} color="primary">
          关闭
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default WelcomeDialog;

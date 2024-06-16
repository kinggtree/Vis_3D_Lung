import React from 'react';
import { Grid, Paper, CircularProgress, Typography } from '@mui/material';

const ImageDisplay = ({ grayImage, maskedImage, isLoading }) => (
  <Grid container spacing={2} className="image-container">
    <Grid item xs={12} direction="column" spacing={2}>
      {isLoading ? (
        <div className="loading-container">
          <CircularProgress />
          <Typography>Loading images...</Typography>
        </div>
      ) : (
        <>
          <Paper elevation={3} className="image-container">
            <img src={grayImage} alt="Gray Image" />
          </Paper>
          <Paper elevation={3} className="image-container">
            <img src={maskedImage} alt="Masked Image" />
          </Paper>
        </>
      )}
    </Grid>
  </Grid>
);

export default ImageDisplay;

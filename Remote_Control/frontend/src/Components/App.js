import React, { useState, useEffect } from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import PauseRounded from '@mui/icons-material/PauseRounded';
import PlayArrowRounded from '@mui/icons-material/PlayArrowRounded';
import VolumeUpRounded from '@mui/icons-material/VolumeUpRounded';
import VolumeDownRounded from '@mui/icons-material/VolumeDownRounded';
import SkipNextRoundedIcon from '@mui/icons-material/SkipNextRounded';
import SkipPreviousRoundedIcon from '@mui/icons-material/SkipPreviousRounded';
import Forward10Icon from '@mui/icons-material/Forward10';
import Replay10Icon from '@mui/icons-material/Replay10';

const Widget = styled('div')(({ theme }) => ({
  padding: 16,
  borderRadius: 16,
  width: 343,
  maxWidth: '100%',
  margin: 'auto',
  position: 'relative',
  zIndex: 1,
}));

export default function App() {
  const [slideVal, setSlideVal] = useState(0);
  const url = 'http://192.168.107.32/'

  useEffect(() => {
    fetch(url + 'cmd/getVol').then((res) => res.text()).then((res) => setSlideVal(parseInt(res)));
  }, [])

  const theme = useTheme();
  theme.palette.mode = 'dark'
  const [paused, setPaused] = useState(true);
  const mainIconColor = theme.palette.mode === 'dark' ? '#fff' : '#000';
  const lightIconColor = theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.4)' : 'rgba(0,0,0,0.4)';

  function run(e) {
    fetch(url + 'cmd/' + e);
  }

  function changeVol(cmd) {
    fetch(url + 'cmd/' + cmd).then((res) => res.text()).then((res) => setSlideVal(res))
  }

  return (
    <>
      <div className="container">
        <button className="btn" id="minus" onClick={() => changeVol('volDown')}></button>
        <button className="btn" id="plus" onClick={() => changeVol('volUp')}></button>
      </div>
      <Box sx={{ width: '100%', overflow: 'hidden' }} className="btnContainer" >
        <Widget>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mt: -1,
            }}
          >
            <IconButton aria-label="previous song" onClick={() => run('prev')} >
              <SkipPreviousRoundedIcon fontSize="large" htmlColor={mainIconColor} />
            </IconButton>
            <IconButton aria-label="backward" onClick={() => run('left')} className='icon' >
              <Replay10Icon fontSize="large" htmlColor={mainIconColor} />
            </IconButton>
            <IconButton
              aria-label={paused ? 'play' : 'pause'}
              onClick={() => { setPaused(!paused); run('playpause') }}
            >
              {paused ? (
                <PlayArrowRounded
                  sx={{ fontSize: '3rem' }}
                  htmlColor={mainIconColor}
                />
              ) : (
                <PauseRounded sx={{ fontSize: '3rem' }} htmlColor={mainIconColor} />
              )}
            </IconButton>
            <IconButton aria-label="next song" onClick={() => run('right')} >
              <Forward10Icon fontSize="large" htmlColor={mainIconColor} />
            </IconButton>
            <IconButton aria-label="forward" onClick={() => run('forward')} >
              <SkipNextRoundedIcon fontSize="large" htmlColor={mainIconColor} />
            </IconButton>
          </Box>
          <Stack spacing={2} direction="row" sx={{ mb: 1, px: 1 }} alignItems="center">
            <VolumeDownRounded htmlColor={lightIconColor} />
            <Slider
              aria-label="Volume"
              defaultValue={slideVal}
              value={slideVal}
              onChange={(e) => setSlideVal(e.target.value)}
              onChangeCommitted={() => fetch(url + 'setVol/' + slideVal)}
              sx={{
                color: theme.palette.mode === 'dark' ? '#fff' : 'rgba(0,0,0,0.87)',
                '& .MuiSlider-track': {
                  border: 'none',
                },
                '& .MuiSlider-thumb': {
                  width: 24,
                  height: 24,
                  backgroundColor: '#fff',
                  '&:before': {
                    boxShadow: '0 4px 8px rgba(0,0,0,0.4)',
                  },
                  '&:hover, &.Mui-focusVisible, &.Mui-active': {
                    boxShadow: 'none',
                  },
                },
              }}
            />
            <VolumeUpRounded htmlColor={lightIconColor} />
          </Stack>
        </Widget>
      </Box>
    </>
  );
}

import Typography from '@material-ui/core/Typography';
import React from "react";

export default function Title (props) {
  return (
    <Typography>
      { props.children }
    </Typography>
  )
}

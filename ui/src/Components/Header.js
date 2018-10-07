import React from "react";
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';




const drawerWidth = 240;

const styles = theme => ({
  appBar: {
    width: `calc(100% - ${drawerWidth}px)`,
  },
  'appBar-left': {
    marginLeft: drawerWidth,
  },
  'appBar-right': {
    marginRight: drawerWidth,
  }
});



class Header extends React.Component {
  render() {
    const { classes } = this.props;

    return (

      <AppBar
        position="absolute"
        className={classNames(classes.appBar, classes[`appBar-left`])}
      >
        <Toolbar>
          <Typography variant="title" color="inherit" noWrap>
            Continuous Organizations
          </Typography>
        </Toolbar>
      </AppBar>

    );
  }
}


Header.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Header);

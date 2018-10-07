import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';


const drawerWidth = 240;

const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  appBar: {
    width: `calc(100% - ${drawerWidth}px)`,
  },
  "appBar-left": {
    marginLeft: drawerWidth,
  },
  "appBar-right": {
    marginRight: drawerWidth,
  },
  drawerPaper: {
    position: "relative",
    width: drawerWidth,
  },
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
  },
});

class Sidebar extends React.Component {
  render() {
    const { classes } = this.props;



    return (

        <Drawer
          variant="permanent"
          classes={{
            paper: classes.drawerPaper,
          }}
          anchor='left'
        >


          <Divider />
      <List>Menu1</List>
          <Divider />
      <List>Menu2</List>
        </Drawer>


    );
  }
}

Sidebar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Sidebar);

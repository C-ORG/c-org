import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';
import Badge from '@material-ui/core/Badge';

const drawerWidth = 240;

const styles = theme => ({
  drawerPaper: {
    position: "relative",
    width: drawerWidth,
    marginTop: "80px"
  },
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
  },
  margin: {
   margin: theme.spacing.unit * 2,
 },
});

class Sidebar extends React.Component {


  render() {
    const { classes, children } = this.props;

    return (
        <Drawer
          variant="permanent"
          classes={{
            paper: classes.drawerPaper,
          }}
        >
          { children }
          <Divider />
          <Typography variant="title" align="center" noWrap>
            Balance
          </Typography>
      <List style={{padding: "15px"}}>
          <Typography align="center" noWrap>ETH
          <Badge className={classes.margin} badgeContent={4} color="primary"/>
          </Typography>
      </List>

      <List style={{padding: "15px"}}>
        <Typography align="center" noWrap>TOK
        <Badge className={classes.margin} badgeContent={10} color="secondary"/>
        </Typography>
      </List>
        </Drawer>


    );
  }
}

Sidebar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Sidebar);

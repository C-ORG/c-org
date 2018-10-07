import React, { Component } from "react";
import "./App.css";
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';

import {Sidebar,
        Graph,
        Header,
        Page,
        Exchange,
        Title,
        Logo} from "./Components";

const styles = theme => ({
  appFrame: {
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex',
    width: '100%',
  },

  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
  },
});

class App extends React.Component {
  render() {
    const { classes } = this.props;



    return (
      <div className="app">
        <div className={classes.appFrame}>
          <Sidebar>
            <Logo />
            <Title />
            <Exchange />
          </Sidebar>

          <Header />

          <Page>
            <Graph />
          </Page>

        </div>
      </div>
    );
  }
}

App.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(App);

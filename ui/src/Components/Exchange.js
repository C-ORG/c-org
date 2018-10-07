import React from 'react';
import TextField from '@material-ui/core/TextField';
import InputAdornment from '@material-ui/core/InputAdornment';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import green from '@material-ui/core/colors/green';



const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  margin: {
    margin: theme.spacing.unit,
  },
  textField: {
    flexBasis: 200,
  },
  button: {
   margin: theme.spacing.unit,
 },
});



class Exchange extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      ether: 0.0,
      token: 0.0,
      sellReserve: 5,
      slope: 1,
      supply: 10,
      disable: false
    };

    this.handleEther = this.handleEther.bind(this);
    this.handleToken = this.handleToken.bind(this);

    this.etherInput = React.createRef();
    this.tokenInput = React.createRef();

  }


  handleToken(event) {
    const token = event.target.value;
    const ether = token * this.state.sellReserve * (2 - token);

    this.setState({token: token});
    this.setState({ether: ether});
  }

  handleEther(event) {
    const ether = event.target.value;
    const token = Math.sqrt(2 * ether / this.state.slope + this.state.supply**2) - this.state.supply;

    this.setState({token: token});
    this.setState({ether: ether});
  }

  render() {
    const { classes } = this.props;
    return (
      <div>
        <Typography variant="title" align="center" noWrap>
          Exchange TOK
        </Typography>
        <TextField
          className={classNames(classes.margin, classes.textField)}
          variant="filled"
          label="Ether"
          value={this.state.ether}
          onChange={this.handleEther}
          InputProps={{
            endAdornment: (
              <InputAdornment variant="filled" position="end">
                ETH
              </InputAdornment>
            ),
          }}
        />

        <TextField
          className={classNames(classes.margin, classes.textField)}
          variant="filled"
          label="Token"
          value={this.state.token}
          onChange={this.handleToken}
          InputProps={{
            endAdornment: (
              <InputAdornment variant="filled" position="end">
                TOK
              </InputAdornment>
            ),
          }}
        />

        <Button variant="contained"  color="primary" href="#contained-buttons" className={classes.button}>
          Buy TOK
        </Button>

        <Button variant="contained"  color="secondary" href="#contained-buttons" className={classes.button}>
          Sell TOK
        </Button>
      </div>
    );
  }
}


Exchange.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Exchange);

import React from 'react';
import Plot from 'react-plotly.js';
import Papa from 'papaparse';

export default class Graph extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: []};
  }


  parseData(url, callBack) {

  }

  componentDidMount() {
    Papa.parse('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv', {
	     download: true,
      dynamicTyping: true,
      complete: results => {
          const rows = results.data;

          function unpack(rows, key) {
              return rows.map(function(row) {
                return row[key];
              });
            }

          var data = [{
            // x: unpack(rows, 'Date'),
            // close: unpack(rows, 'AAPL.Close'),
            // high: unpack(rows, 'AAPL.High'),
            // low: unpack(rows, 'AAPL.Low'),
            // open: unpack(rows, 'AAPL.Open'),

            x: unpack(rows, 0),
            close: unpack(rows, 4),
            high: unpack(rows, 2),
            low: unpack(rows, 3),
            open: unpack(rows, 1),

            // cutomise colors
            increasing: {line: {color: 'green'}},
            decreasing: {line: {color: 'red'}},

            type: 'candlestick',
            xaxis: 'x',
            yaxis: 'y'
          }];
          this.setState( {data: data} );
        }
      });
  }

  render() {
      return (
          <Plot
              data={this.state.data}
              layout={{width: 800, height: 400}}
              // onInitialized={(figure) => this.setState(figure)}
              // onUpdate={(figure) => this.setState(figure)}
          />
      );
  }

  //
  // render() {
  //   return (
  //     <Plot
  //       data={[
  //         {
  //           x: [1, 2, 3],
  //           y: [2, 6, 3],
  //           type: 'scatter',
  //           mode: 'lines+points',
  //           marker: {color: 'red'},
  //         },
  //         {type: 'candlestick', x: [1, 2, 3], y: [2, 5, 3]},
  //       ]}
  //       layout={ {width: "800", height: 400} }
  //     />
  //   );
  // }
}

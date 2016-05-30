// Karma configuration
// Generated on Mon Mar 28 2016 15:58:49 GMT-0500 (ECT)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      //'../bower_components/jquery/dist/jquery.js',
      '../bower_components/angular/angular.js',
      '../bower_components/angular-mocks/angular-mocks.js',
      '../bower_components/angular-route/angular-route.js',
      '../bower_components/angular-cookies/angular-cookies.js',
      '../bower_components/angular-material/angular-material.js',
      '../bower_components/angular-animate/angular-animate.js',
      '../bower_components/angular-aria/angular-aria.js',
      '../bower_components/angular-sanitize/angular-sanitize.js',
      'app/fotuto-app.js',
      'shared/*.filters.js',
      'components/**/controller.js',
      'components/**/*.directives.js',
      'components/**/*.html',
      // Files in other django apps
      '../../**/static/spa/components/**/*.directives.js',
      '../../**/static/spa/components/**/*.controllers.js',
      '../../**/static/spa/components/**/*.filters.js',
      '../../**/static/spa/components/**/*.html',

      // test files
      'app/*_test.js',
      'shared/*_test.js',
      'components/**/*_test.js',
      '../../**/static/spa/components/**/*_test.js'  // tests inside django packages
    ],


    // list of files to exclude
    exclude: [
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
      'components/**/*.html': ['ng-html2js'],
      //'../../**/static/spa/components/**/*.html': ['ng-html2js']
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['Chrome'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false,

    // Concurrency level
    // how many browser should be started simultaneous
    concurrency: Infinity,

    ngHtml2JsPreprocessor: {
      // setting this option will create only a single module that contains templates
      // from all the files, so you can load them all with module('templates')
      moduleName: 'templates',
      cacheIdFromPath: function(filepath) {
        return '/static/spa/' + filepath;
      }
    }
  })
};

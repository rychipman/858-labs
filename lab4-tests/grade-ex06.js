var fs = require("fs");
var system = require("system");
var webpage = require("webpage");

var grading = require("./grading");

function main(studentDir) {
    if (studentDir === undefined) {
        console.log("USAGE: phantomjs " + system.args[0] + " student_dir/");
        phantom.exit();
        return;
    }
    var answerPath = studentDir + "/answer-6.html";
    if (!fs.isFile(answerPath)) {
        grading.failed("No answer-6.html");
        phantom.exit();
        return;
    }

    grading.registerTimeout();

    // Initialize the world.
    grading.initUsers(function(auth) {
        // The grader (victim) will already be logged in to the zoobar
        // site before loading your page.
        phantom.cookies = auth.graderCookies;

        // Open the attacker's page.
        var page = webpage.create();

        page.onLoadFinished = function(status) {

            // Check that the grader now has no zoobars.
            grading.getZoobars(function(number) {
                if (number != 0) {
                    grading.failed("grader has " + number + " zoobars, should have 0");
                } else {
                    grading.passed("grader zoobar count");
                }

                // Check that the attacker now has 20.
                phantom.cookies = auth.attackerCookies;
                grading.getZoobars(function(number) {
                    if (number != 20) {
                        grading.failed("attacker has " + number + " zoobars, should have 20");
                    } else {
                        grading.passed("attacker zoobar count");
                    }

                    phantom.exit();
                });
            });
        };

        page.open(answerPath, function(status) {

            page.evaluate(function() {
                if (document.forms.length != 1) {
                    grading.failed("answer-6.html has more than one form!");
                    phantom.exit();
                }
                document.forms[0].submit();
            });
        });





    });
}

main.apply(null, system.args.slice(1));

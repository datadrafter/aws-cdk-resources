import aws_cdk.aws_quicksight as quicksight

# data_driven: Any

cfn_dashboard = quicksight.CfnDashboard(self, "MyCfnDashboard",
    aws_account_id="awsAccountId",
    dashboard_id="dashboardId",
    name="name",
)

# the properties below are optional
dashboard_publish_options=quicksight.CfnDashboard.DashboardPublishOptionsProperty(
    ad_hoc_filtering_option=quicksight.CfnDashboard.AdHocFilteringOptionProperty(
        availability_status="availabilityStatus"
    ),
    data_point_drill_up_down_option=quicksight.CfnDashboard.DataPointDrillUpDownOptionProperty(
        availability_status="availabilityStatus"
    ),
    data_point_menu_label_option=quicksight.CfnDashboard.DataPointMenuLabelOptionProperty(
        availability_status="availabilityStatus"
    ),
    data_point_tooltip_option=quicksight.CfnDashboard.DataPointTooltipOptionProperty(
        availability_status="availabilityStatus"
    ),
    export_to_csv_option=quicksight.CfnDashboard.ExportToCSVOptionProperty(
        availability_status="availabilityStatus"
    ),
    export_with_hidden_fields_option=quicksight.CfnDashboard.ExportWithHiddenFieldsOptionProperty(
        availability_status="availabilityStatus"
    ),
    sheet_controls_option=quicksight.CfnDashboard.SheetControlsOptionProperty(
        visibility_state="visibilityState"
    ),
    sheet_layout_element_maximization_option=quicksight.CfnDashboard.SheetLayoutElementMaximizationOptionProperty(
        availability_status="availabilityStatus"
    ),
    visual_axis_sort_option=quicksight.CfnDashboard.VisualAxisSortOptionProperty(
        availability_status="availabilityStatus"
    ),
    visual_menu_option=quicksight.CfnDashboard.VisualMenuOptionProperty(
        availability_status="availabilityStatus"
    ),
    visual_publish_options=quicksight.CfnDashboard.DashboardVisualPublishOptionsProperty(
        export_hidden_fields_option=quicksight.CfnDashboard.ExportHiddenFieldsOptionProperty(
            availability_status="availabilityStatus"
        )
    )
)


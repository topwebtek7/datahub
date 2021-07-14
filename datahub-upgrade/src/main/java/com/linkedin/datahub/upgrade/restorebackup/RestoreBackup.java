package com.linkedin.datahub.upgrade.restorebackup;

import com.google.common.collect.ImmutableList;
import com.linkedin.datahub.upgrade.Upgrade;
import com.linkedin.datahub.upgrade.UpgradeCleanupStep;
import com.linkedin.datahub.upgrade.UpgradeStep;
import com.linkedin.datahub.upgrade.common.steps.ClearGraphServiceStep;
import com.linkedin.datahub.upgrade.common.steps.ClearSearchServiceStep;
import com.linkedin.datahub.upgrade.common.steps.GMSDisableWriteModeStep;
import com.linkedin.datahub.upgrade.common.steps.GMSEnableWriteModeStep;
import com.linkedin.datahub.upgrade.common.steps.GMSQualificationStep;
import com.linkedin.entity.client.EntityClient;
import com.linkedin.metadata.entity.EntityService;
import com.linkedin.metadata.graph.GraphService;
import com.linkedin.metadata.models.registry.EntityRegistry;
import com.linkedin.metadata.search.SearchService;
import io.ebean.EbeanServer;
import java.util.ArrayList;
import java.util.List;


public class RestoreBackup implements Upgrade {

  private final List<UpgradeStep> _steps;

  public RestoreBackup(final EbeanServer server, final EntityService entityService, final EntityRegistry entityRegistry,
      final EntityClient entityClient, final GraphService graphClient, final SearchService searchClient) {
    _steps = buildSteps(server, entityService, entityRegistry, entityClient, graphClient, searchClient);
  }

  @Override
  public String id() {
    return "RestoreBackup";
  }

  @Override
  public List<UpgradeStep> steps() {
    return _steps;
  }

  private List<UpgradeStep> buildSteps(final EbeanServer server, final EntityService entityService,
      final EntityRegistry entityRegistry, final EntityClient entityClient, final GraphService graphClient,
      final SearchService searchClient) {
    final List<UpgradeStep> steps = new ArrayList<>();
    steps.add(new GMSQualificationStep());
    steps.add(new GMSDisableWriteModeStep(entityClient));
    steps.add(new ClearSearchServiceStep(searchClient, true));
    steps.add(new ClearGraphServiceStep(graphClient, true));
    steps.add(new ClearAspectV2TableStep(server));
    steps.add(new RestoreStorageStep(entityService, entityRegistry));
    steps.add(new GMSEnableWriteModeStep(entityClient));
    return steps;
  }

  @Override
  public List<UpgradeCleanupStep> cleanupSteps() {
    return ImmutableList.of();
  }
}
